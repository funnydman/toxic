import re
from http.server import HTTPServer
from inspect import signature
from typing import Callable, Tuple

from toxic.core import status
from toxic.core.exceptions import HTTPException
from toxic.core.request import Request
from toxic.core.resource import Router
from toxic.core.server.main import RequestHandler


class HTTPRequestHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = HTTPRequestHandler()

    def handle(self) -> None:
        super().handle()
        self._handle_one_request()

    def process_request(
            self,
            handler,
            request: Request,
            params: dict,
    ) -> Callable:
        _handler = getattr(handler.handler_cls(), request.method.lower(), None)
        if _handler is None:
            self.send_error(code=status.HTTP_NOT_FOUND, message='method is not allowed')
            raise HTTPException(detail='method is not allowed')

        params = {**params, 'request': request}

        params_to_inject = self.__get_injection_params(_handler, params)
        try:
            result = _handler(**params_to_inject)
            return result
        except Exception as e:
            self.send_error(code=status.HTTP_SERVER_ERROR, explain=str(e))
            raise

    def find_handler_by_path(self, path: str) -> Tuple[Router, dict]:
        for router in self.app.routers_collection:
            for r in router.routers:
                match = re.match(r.path, path)
                if match:
                    params = match.groupdict()
                    return r, params
        # raise 404
        self.send_error(code=404)

    def _handle_one_request(self):

        handler, params = self.find_handler_by_path(self.request.path)

        response = self.process_request(handler, self.request, params)

        self._send_response(response)

    def send_begin_header(self, status_code):
        self._header_buffer = []
        _header_str = f'HTTP/1.0 {status_code}\r\n'
        self._header_buffer.append(_header_str.encode())

    def __end_headers(self):
        self._header_buffer.append(b"\r\n")
        _headers_str = b"".join(self._header_buffer)
        self.wfile.write(_headers_str)
        # clear the buffer
        self._header_buffer = []

    def __get_injection_params(self, handler, params=None):
        try:
            expected_params = signature(handler).parameters
            passed_keys = set(expected_params.keys()) & set(params.keys())
            result = {k: v for k, v in params.items() if k in passed_keys}
            if 'request' in expected_params:
                result['request'] = params['request']

            return result
        except Exception as e:
            self.send_error(code=500, explain=str(e))


class Server:
    def __init__(self, server_class, handler_class):
        self.server_class = server_class
        self.handler_class = handler_class

    def run(self, app, host='', port=8000):
        server_address = (host, port)
        httpd = self.server_class(server_address, self.handler_class)
        self.handler_class.app = app

        httpd.serve_forever()


server = Server(HTTPServer, HTTPRequestHandler)
