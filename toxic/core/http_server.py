import io
import re
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from inspect import signature
from typing import Callable

from toxic.core.request import Request


class HTTPRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def construct_response_header():
        # Todo: proper implementation
        headers = [
            b'HTTP/1.0 200 OK\r\n',
            b'Server: SimpleHTTP/0.6 Python/3.8.2\r\n',
            b'Date: Fri, 15 May 2020 20:18:36 GMT\r\n',
            b'Content-type: application/json; charset=utf-8\r\n',
            b'Content-Length: 200\r\n',
            b'\r\n'
        ]
        return headers

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def __handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

        except TimeoutError as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True

    def get_handler(self, handler, method: str) -> Callable:
        _handler = getattr(handler.handler_cls(), method.lower())
        if _handler is None:
            self.send_error(code=404, message='method is not allowed')
        return _handler

    def find_handler_by_path(self, path: str):
        for router in self.app.routers_collection:
            for r in router.routers:
                match = re.match(r.path, path)
                if match:
                    params = match.groupdict()
                    return r, params
        # raise 404
        self.send_error(code=404)

    def handle_one_request(self):
        self.__handle_one_request()

        headers = self.construct_response_header()

        _request = Request(
            method=self.command,
            path=self.path,
            headers=self.headers
        )

        handler, params = self.find_handler_by_path(_request.path)

        handler = self.get_handler(handler, self.command)

        response = self.call_handler(handler, params=params)

        f = io.BytesIO(response.render().encode())
        f = io.BufferedReader(f)

        to_send = b"".join(headers)
        self.wfile.write(to_send)
        self.wfile.write(f.read())
        self.wfile.flush()  # actually send the response if not already done.

        self.log_request(200)

    def __send_response(self) -> None:
        return

    def call_handler(self, handler, params=None):
        try:
            expected_params = signature(handler).parameters
            passed_keys = set(expected_params.keys()) & set(params.keys())
            result = {k: v for k, v in params.items() if k in passed_keys}
            if 'request' in expected_params:
                # pass request
                result['request'] = {}

            result = handler(**result)
            return result
        except Exception as e:
            self.send_error(code=500, explain=str(e))


class Server:
    def __init__(self, server_class, handler_class):
        self.server_class = server_class
        self.handler_class = handler_class

    def run(self, app):
        server_address = ('', 8000)
        httpd = self.server_class(server_address, self.handler_class)
        self.handler_class.app = app

        httpd.serve_forever()


server = Server(HTTPServer, HTTPRequestHandler)
