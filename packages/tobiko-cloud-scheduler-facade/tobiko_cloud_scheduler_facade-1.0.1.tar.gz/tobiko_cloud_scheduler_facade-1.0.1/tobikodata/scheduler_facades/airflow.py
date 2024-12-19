import time
import typing as t
from functools import cached_property

from airflow import DAG
from airflow.exceptions import AirflowFailException, AirflowNotFoundException, AirflowSkipException
from airflow.models import BaseOperator
from airflow.models.connection import Connection
from airflow.models.taskinstance import TaskInstance
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from airflow.utils.trigger_rule import TriggerRule
from sqlglot import exp

from tobikodata.http_client import V1ApiClient
from tobikodata.http_client.api_models.v1.dags import V1DagNode
from tobikodata.http_client.api_models.v1.evaluations import V1RunEvaluation
from tobikodata.scheduler_facades.common import create_api_client


def _wait_until_next_remote_run(ti: TaskInstance, conn_id: str, environment: str) -> bool:
    """
    Intended to be called by a PythonSensor in order to block until a remote run is available to report on
    """
    import logging

    logger = logging.getLogger(__name__)

    api = SQLMeshEnterpriseAirflow(conn_id=conn_id).api

    logger.info(f"Fetching last remote run for environment: {environment}")
    last_remote_run = api.runs.get_last_run_for_environment(environment=environment)

    # Note that `include_prior_dates` seems to just return a single value from the last run and not an array of values from every historical run
    # This approach allows us to avoid reporting on the same run over and over while still being able to report on runs that start and finish
    # before we even get a chance to poll (and thus wouldnt show if we were only looking for in-progress runs)
    last_airflow_run_id = ti.xcom_pull(key="run_id", include_prior_dates=True)
    logger.info(f"Last run id we reported on: {last_airflow_run_id}")

    if last_remote_run:
        logger.info(f"Last run in Tobiko Cloud: {last_remote_run.run_id}")

        if last_remote_run.run_id != last_airflow_run_id:
            # We havent reported on this run yet, let's do it
            run_id = last_remote_run.run_id
            logger.info(f"View realtime output on Tobiko Cloud: {last_remote_run.link}")
            ti.xcom_push("run_id", run_id)
            return True
        else:
            logger.info(
                f"We have already reported on run '{last_remote_run.run_id}'; waiting for new run"
            )
    else:
        logger.warning(f"No runs in Tobiko Cloud for environment: {environment}")

    return False


def _report(conn_id: str, run_id: str, node_name: str) -> None:
    """
    Intended to be called by a PythonOperator to report on the status of a task in the remote run
    """
    import logging

    logger = logging.getLogger(__name__)

    api = SQLMeshEnterpriseAirflow(conn_id=conn_id).api

    if not run_id:
        raise AirflowFailException(
            "Unable to fetch run_id that should have been populated by the sensor task"
        )

    logger.info(f"Run: '{run_id}'; Node: '{node_name}'")

    remote_run = api.runs.get_run_by_id(run_id)
    if not remote_run:
        raise AirflowFailException(f"Run with id {run_id} does not exist in Tobiko Cloud")

    def _wait_until_ended() -> t.Optional[t.List[V1RunEvaluation]]:
        # block until evaluation has ended which means we can mark this task as complete and move on
        # there isnt always anything to evaluate either (eg a model with a daily cadence will only get evaluated once per day even if we are running every 5mins)
        while True:
            # an evaluation is created per batch, meaning there can be multiple evaluation records for each snapshot in the run
            if our_evaluations := api.runs.get_evaluations_for_node(run_id, node_name):
                complete = [e for e in our_evaluations if e.end_at]
                incomplete = [e for e in our_evaluations if e not in complete]
                if incomplete:
                    # check if the run has actually finished. if the remote scheduler crashes, sometimes the evaluation record isnt updated
                    # to have an end_at but the run record is marked as completed with an error message
                    if remote_run.end_at:
                        if remote_run.error_message:
                            logger.error(f"Run '{run_id}' has failed with:")
                            logger.error(remote_run.error_message)
                            raise AirflowFailException(f"Run '{run_id}' failed remotely")

                        # run finished without setting an end_at on this record?
                        raise AirflowSkipException()
                    else:
                        logger.info(
                            f"{len(complete)}/{len(our_evaluations)} evaluations have completed for this snapshot; waiting"
                        )
                        time.sleep(5)
                        continue
                return complete

            return None

    if complete_evaluations := _wait_until_ended():
        any_failed = False

        for evaluation in complete_evaluations:
            if evaluation.error_message:
                logger.error(f"Evaluation failed: {evaluation.error_message}")
                logger.error(f"View more information in Tobiko Cloud: {evaluation.link}")
                any_failed = True
            else:
                logger.info("Evaluation completed successfully")
                logger.info(f"View the log output in Tobiko Cloud: {evaluation.log_link}")

        if any_failed:
            # so Airflow marks this task as failed and doesnt bother retrying
            raise AirflowFailException()
    else:
        logger.info("No evaluation record for this model; skipping")
        raise AirflowSkipException()


class SQLMeshEnterpriseAirflow:
    """
    Generate an Airflow DAG based on a to Tobiko Cloud project

    Usage:

    ```python
    from tobikodata.sqlmesh_enterprise.intergrations.airflow import SQLMeshEnterpriseAirflow

    first_task, last_task, dag = SQLMeshEnterpriseAirflow().create_cadence_dag()

    # from here, you can add tasks to run before the first task and after the last task like so:
    extra_task = EmptyOperator()
    last_task >> extra_task
    ```
    """

    def __init__(self, conn_id: str = "tobiko_cloud"):
        """
        :conn_id - Airflow connection ID containing the Tobiko Cloud connection details

        The connection should be set up like so:

        - type: http
          host: https://cloud.tobikodata.com/your/project/root
          password: <tobiko cloud token>
        """
        self.conn_id = conn_id

    @cached_property
    def config(self) -> Connection:
        # will raise AirflowNotFoundException if the user has not created conn_id
        return Connection.get_connection_from_secrets(conn_id=self.conn_id)

    @property
    def api(self) -> V1ApiClient:
        return create_api_client(base_url=self.config.host, token=self.config.password)

    def create_cadence_dag(
        self,
        environment: str = "prod",
        dag_kwargs: t.Dict[str, t.Any] = {},
        common_task_kwargs: t.Dict[str, t.Any] = {},
        sensor_task_kwargs: t.Dict[str, t.Any] = {},
        report_task_kwargs: t.Dict[str, t.Any] = {},
    ) -> t.Tuple[BaseOperator, BaseOperator, DAG]:
        env = self.api.dags.get_dag_for_environment(environment)
        if not env:
            raise AirflowNotFoundException(
                f"The environment '{environment}' is not present in Tobiko Cloud. Has a plan been run on it yet?"
            )

        dag_kwargs.setdefault("dag_id", f"{self.conn_id}_{environment}")
        dag_kwargs.setdefault(
            "description", f"SQLMesh cadence run for the '{environment}' environment"
        )
        dag_kwargs.setdefault("start_date", env.start_at)
        dag_kwargs.setdefault("schedule", env.schedule_cron)
        dag_kwargs.setdefault("catchup", False)
        dag_kwargs.setdefault("max_active_runs", 1)

        with DAG(
            **dag_kwargs,
        ) as dag:
            sensor_task = self._create_wait_for_run_sensor_task(
                environment, **{**common_task_kwargs, **sensor_task_kwargs}
            )

            report_tasks = {
                n.name: (
                    n,
                    self._create_report_task(n, **{**common_task_kwargs, **report_task_kwargs}),
                )
                for n in env.nodes
            }

            for node, task in report_tasks.values():
                for parent_name in node.parent_names:
                    _, parent_task = report_tasks[parent_name]
                    parent_task >> task

            join_task = self._create_synchronisation_point_task(**common_task_kwargs)

            tasks_with_no_parents = [
                task for _, task in report_tasks.values() if not task.upstream_task_ids
            ]
            tasks_with_no_children = [
                task for _, task in report_tasks.values() if not task.downstream_task_ids
            ]

            for task in tasks_with_no_parents:
                sensor_task >> task

            for task in tasks_with_no_children:
                task >> join_task

            return sensor_task, join_task, dag

    def _create_wait_for_run_sensor_task(
        self, environment: str, **task_kwargs: t.Any
    ) -> PythonSensor:
        return PythonSensor(
            task_id="wait_until_ready",
            python_callable=_wait_until_next_remote_run,
            op_kwargs={"conn_id": self.conn_id, "environment": environment},
            poke_interval=5,  # poll every 5 seconds
            **task_kwargs,
        )

    def _create_report_task(self, node: V1DagNode, **report_task_kwargs: t.Any) -> PythonOperator:
        task_id = node.name.replace('"', "")

        return PythonOperator(
            task_id=task_id,
            task_display_name=exp.to_table(node.name).name,
            python_callable=_report,
            op_kwargs={
                "conn_id": self.conn_id,
                "run_id": '{{ ti.xcom_pull(key="run_id") }}',
                "node_name": node.name,
            },
            trigger_rule=TriggerRule.ALL_DONE,  # to enable these tasks to reflect the remote state regardless of the state of upstream tasks in Airflow
            **report_task_kwargs,
        )

    def _create_synchronisation_point_task(self, **task_kwargs: t.Any) -> EmptyOperator:
        # this is just a synchronisation point so that a user can tack on extra tasks once all snapshots finish,
        # even if there are a bunch running in parallel because they dont depnd on each other
        return EmptyOperator(task_id="finish", trigger_rule=TriggerRule.ALL_DONE, **task_kwargs)
