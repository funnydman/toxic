allowed_http_methods = frozenset({'OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'})


class HTTPRequestHandler:
    def __init__(self, method: str, request_uri: str) -> None:

        self.method = method
        self.request_uri = request_uri

    def __call__(self):
        if self.method not in allowed_http_methods:
            raise RuntimeError('Method is not allowed')

        _handler = getattr(self, self.method.lower(), None)
        if not _handler:
            raise RuntimeError('There is no such handler')
        return _handler

    def get(self):
        self.server.wfile.write(b'HTTP/1.1 200 OK\r\n\r\n')


class WsgiRequestHandler():
    pass
