# Ascender HTTP Client (aschttp)

**`ascender-httpclient`** (aschttp) is a powerful and extendable HTTP client for the **Ascender Framework**. It supports synchronous, asynchronous, and streaming HTTP requests with clean dependency injection, interceptors, and multi-instance configurations.

## Features

- **Dependency Injection**: Easily inject `HTTPClient` into any service.
- **Interceptor Support**: Create and manage interceptors to customize request handling.
- **Multiple HTTPClient Instances**: Use custom HTTP client classes alongside the default singleton.
- **Async and Streaming Requests**: Built-in support for asynchronous and streaming HTTP requests.
- **Command Line Integration**: Generate interceptors with a simple CLI command.

---

## Installation

To install the package, in your project type:
```bash
poetry add ascender-httpclient
```

Ensure that the **Ascender Framework** is installed and properly configured.

---

## Initialization

To initialize `aschttp`, configure `ProvideHTTPClient()` in your `bootstrap.py`:

```python
...
from aschttp import ProvideHTTPClient

appBootstrap: IBootstrap = {
    "providers": [
        DatabaseProvider(ORMEnum.SQLALCHEMY, DATABASE_CONNECTION),
        ProvideControllers([
            ControllersModule
        ]),
        ProvideHTTPClient()
    ]
}
```

---

## Usage

### Injecting `HTTPClient`

To inject the HTTP client into any service:
```python
from ascender.common import Injectable
from ascender.contrib.services import Service
from aschttp import HTTPClient

@Injectable()
class MainService(Service):
    def __init__(self, http: HTTPClient):
        self.http = http
```

### Making Requests

#### GET Request

```python
from controllers.dtos.test_dto import TestDTO

@Injectable()
class MainService(Service):
    def __init__(self, http: HTTPClient):
        self.http = http
    
    async def make_get_request(self):
        response = await self.http.get(TestDTO, url="http://api.example.com/get")
        assert isinstance(response, TestDTO)
        return response
```

#### POST Request

```python
from controllers.dtos.test_dto import TestDTO

@Injectable()
class MainService(Service):
    def __init__(self, http: HTTPClient):
        self.http = http
    
    async def make_post_request(self, dto: TestDTO):
        response = await self.http.post(str, url="http://api.example.com/post", content=dto)
        assert isinstance(response, str)
        return response
```

#### Streaming Request

```python
@Injectable()
class MainService(Service):
    def __init__(self, http: HTTPClient):
        self.http = http
    
    def make_streaming_request(self):
        self.http.stream(str, method="GET", url="http://api.example.com/stream").subscribe(
            on_next=lambda r: print(r),
            on_error=lambda err: print(err)
        )
```

---

## Custom HTTP Clients

To use multiple HTTP client instances:

1. Define a custom HTTP client class:
```python
from aschttp import HTTPClient

class MyHTTP(HTTPClient):
    pass
```

2. Register the custom HTTP client in `bootstrap.py`:
```python
from myclient import MyHTTP

appBootstrap: IBootstrap = {
    "providers": [
        ProvideHTTPClient(),
        ProvideHTTPClient(client_instance=MyHTTP)
    ]
}
```

---

## Interceptors

Interceptors allow you to modify HTTP requests before they are sent.

### Generate an Interceptor

Use the Ascender CLI to generate an interceptor:
```bash
ascender run aschttp:generate interceptor interceptors/custom
```
**Output:**
```
$ CREATE interceptors/custom_interceptor.py (164 bytes)
```

### Implementing an Interceptor

Example custom interceptor:
```python
from httpx import Request
from aschttp.types.interceptors import Interceptor

class CustomInterceptor(Interceptor):
    def __init__(self) -> None:  # for dependency injection, REQUIRED
        pass

    async def handle_request(self, request: Request) -> Request:
        # Modify the request here...
        print("custom interceptor works!")
        return request
```

### Registering an Interceptor

Register the interceptor in `bootstrap.py`:
```python
from processes.custom_interceptor import MyInterceptor

appBootstrap: IBootstrap = {
    "providers": [
        ProvideHTTPClient(interceptors=[
            MyInterceptor
        ])
    ]
}
```

---

## Key Concepts

### Singleton HTTPClient
The `HTTPClient` is a singleton by default, ensuring a single instance throughout the framework. However, you can register multiple clients using the `ProvideHTTPClient` factory, all you need is to change it's `client_instance` parameter into your custom, example provided in [Custom HTTP Clients](#Custom-HTTP-Clients) section.

### Interceptors
Interceptors allow request modification before sending. Use them for:
- Adding headers
- Logging requests
- Transforming request payloads

### Streaming
The `stream()` method uses an observable pattern to handle streaming responses efficiently utilizing RxPY.

---

## Command Reference

### Generate Interceptor
```bash
ascender run aschttp:generate interceptor <path/to/interceptor>
```

---

## Examples Repository

Find more examples and best practices in the official **Ascender Framework** examples repository.

---

## Contribution

Contributions are welcome! Submit issues, feature requests, or pull requests via GitHub.

---

## License

The `ascender-httpclient` package is licensed under the MIT License.
