from typing import Optional


class HttpRequest:
    def __init__(
        self,
        url: str,
        method: str,
        headers: dict,
        body: Optional[str],
        timeout: int,
        retries: int,
        auth_token: Optional[str],
        proxy: Optional[str],
        ssl_verify: bool,
        follow_redirects: bool,
        cache_ttl: int,
        compression: Optional[str],
    ):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.retries = retries
        self.auth_token = auth_token
        self.proxy = proxy
        self.ssl_verify = ssl_verify
        self.follow_redirects = follow_redirects
        self.cache_ttl = cache_ttl
        self.compression = compression


def send_http(req: HttpRequest):
    return f"Response from {req.url}"


class HttpRequestBuilder:
    def __init__(self):
        self._url = None
        self._method = "GET"
        self._headers = {}
        self._body = None
        self._timeout = 30
        self._retries = 3
        self._auth_token = None
        self._proxy = None
        self._ssl_verify = True
        self._follow_redirects = True
        self._cache_ttl = 0
        self._compression = None

    def url(self, url: str):
        self._url = url
        return self

    def method(self, method: str):
        self._method = method
        return self

    def headers(self, headers: dict):
        self._headers = headers
        return self

    def body(self, body: str):
        self._body = body
        return self

    def build(self) -> HttpRequest:
        if not self._url:
            raise ValueError("URL is required")

        return HttpRequest(
            url=self._url,
            method=self._method,
            headers=self._headers,
            body=self._body,
            timeout=self._timeout,
            retries=self._retries,
            auth_token=self._auth_token,
            proxy=self._proxy,
            ssl_verify=self._ssl_verify,
            follow_redirects=self._follow_redirects,
            cache_ttl=self._cache_ttl,
            compression=self._compression,
        )


class Handler:
    def handle(self, req: HttpRequest):
        raise NotImplementedError


class NullHandler(Handler):
    def handle(self, req: HttpRequest):
        return send_http(req)


class Middleware(Handler):
    def __init__(self, next_handler: Handler):
        self._next = next_handler

    def handle(self, req: HttpRequest):
        return self._next.handle(req)


class LogMiddleware(Middleware):
    def handle(self, req: HttpRequest):
        print("Logging request")
        return super().handle(req)


class AuthMiddleware(Middleware):
    def handle(self, req: HttpRequest):
        print("Authenticating")
        return super().handle(req)


class CacheMiddleware(Middleware):
    def handle(self, req: HttpRequest):
        print("Cache check")
        return super().handle(req)


class RetryMiddleware(Middleware):
    def handle(self, req: HttpRequest):
        print("Retry logic")
        return super().handle(req)


class CompressMiddleware(Middleware):
    def handle(self, req: HttpRequest):
        print("Compression applied")
        return super().handle(req)


def build_pipeline(middlewares: list) -> Handler:
    handler: Handler = NullHandler()

    for middleware_cls in reversed(middlewares):
        handler = middleware_cls(handler)

    return handler


def execute_request(req: HttpRequest, middlewares: list):
    pipeline = build_pipeline(middlewares)
    return pipeline.handle(req)


if __name__ == "__main__":
    req = (
        HttpRequestBuilder()
        .url("https://example.com")
        .method("GET")
        .headers({"Accept": "application/json"})
        .build()
    )

    middlewares = [
        LogMiddleware,
        AuthMiddleware,
        CacheMiddleware,
        RetryMiddleware,
        CompressMiddleware,
    ]

    response = execute_request(req, middlewares)
    print(response)