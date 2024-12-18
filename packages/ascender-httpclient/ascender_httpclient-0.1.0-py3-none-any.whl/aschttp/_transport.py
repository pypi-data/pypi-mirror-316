from inspect import isawaitable, isclass
import ssl
from typing import Any, cast
from httpx import AsyncBaseTransport, Request, AsyncHTTPTransport
from httpx._models import Response
from httpx._types import CertTypes, ProxyTypes
from httpx._config import Limits, DEFAULT_LIMITS

from aschttp.types.interceptors import Interceptor, InterceptorFn
from ascender.core.registries.service import ServiceRegistry


class AscHTTPTransport(AsyncBaseTransport):
    def __init__(
        self,
        interceptors: list[InterceptorFn | type[Interceptor]] = [],
        verify: ssl.SSLContext | str | bool = True,
        cert: CertTypes | None = None,
        trust_env: bool = True,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        proxy: ProxyTypes | None = None,
        uds: str | None = None,
        local_address: str | None = None,
        retries: int = 0,
        socket_options: Any | None = None,
    ) -> None:
        super().__init__()
        self.interceptors = interceptors
        self.transport = AsyncHTTPTransport(verify=verify, cert=cert, trust_env=trust_env,
                                            http1=http1, http2=http2, limits=limits,
                                            proxy=proxy, uds=uds, local_address=local_address,
                                            retries=retries, socket_options=socket_options)

    async def handle_async_request(self, request: Request) -> Response:
        # Request modification
        modified_request = request
        for interceptor in self.interceptors:
            if isclass(interceptor) and issubclass(cast(type[Interceptor], interceptor), Interceptor):
                dependencies = ServiceRegistry().get_parameters(interceptor)
                interceptor_instance = interceptor(**dependencies)

                modified_request = await interceptor_instance.handle_request(request)
                continue

            modified_request = await interceptor(request) # type: ignore
        
        response = await self.transport.handle_async_request(modified_request)
        return response
    
    async def aclose(self) -> None:
        return await self.transport.aclose()