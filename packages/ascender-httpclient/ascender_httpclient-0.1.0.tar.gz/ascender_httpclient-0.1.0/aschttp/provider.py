import ssl
from typing import Any
from aschttp._transport import AscHTTPTransport
from aschttp.types.interceptors import Interceptor, InterceptorFn
from .client import HTTPClient
from httpx._types import CertTypes


class ProvideHTTPClient:
    def __new__(
        cls,
        base_url: str = "",
        interceptors: list[InterceptorFn | type[Interceptor]] = [],
        verify: ssl.SSLContext | str | bool = True,
        cert: CertTypes | None = None,
        trust_env: bool = True,
        client_instance: type[HTTPClient] = HTTPClient
    ) -> HTTPClient:
        
        client = client_instance(base_url, AscHTTPTransport(
            interceptors=interceptors,
            verify=verify,
            cert=cert,
            trust_env=trust_env
        ))
        return client