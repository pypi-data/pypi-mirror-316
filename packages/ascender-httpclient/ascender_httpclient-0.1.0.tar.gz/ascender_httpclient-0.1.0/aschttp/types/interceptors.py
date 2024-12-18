from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Coroutine
from httpx import Request

InterceptorIn = Request
InterceptorFn = Awaitable[Callable[[Request], Request]]


class Interceptor(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        ...
    
    @abstractmethod
    async def handle_request(self, request: InterceptorIn) -> Request:
        raise NotImplementedError("Handle request is not implemented")