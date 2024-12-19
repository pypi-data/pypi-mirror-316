import typing as t

import httpx

from tobikodata.helpers import urljoin
from tobikodata.http_client import BearerAuth, HttpClient, V1ApiClient


def create_api_client(
    base_url: t.Optional[str] = None,
    token: t.Optional[str] = None,
    headers: t.Optional[t.Dict[str, str]] = None,
    client: t.Optional[httpx.Client] = None,
) -> V1ApiClient:
    auth = BearerAuth(token=token) if token else None

    if client and not base_url:
        base_url = str(client.base_url)

    if not base_url:
        raise ValueError("base_url must be supplied if no pre-configured http client is supplied")

    if not client:
        # note: follow_redirects is enabled because it offers the best user experience in corporate networks
        # when its almost guaranteed there is some kind of proxy messing with the traffic
        # in addition, FastAPI automatically redirects from route("") to route("/") if route("") isnt defined
        # which raises an exception in httpx.Client unless follow_redirects is enabled
        client = httpx.Client(base_url=base_url, follow_redirects=True)

    client_wrapper = HttpClient(
        auth=auth,
        headers=headers,
        health_ready=urljoin(base_url, "api/state-sync/enterprise-version"),
        client=client,
    )

    return V1ApiClient(client_wrapper)
