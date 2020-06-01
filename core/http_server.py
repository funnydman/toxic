import io
import json
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable

from core.request import Request


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

    def get_handler(self, handler) -> Callable:
        return getattr(handler.handler_cls(), handler.method.lower())

    def handle_one_request(self):
        self.__handle_one_request()

        headers = self.construct_response_header()
        # todo: find out right handler or request

        _request = Request(
            method=self.command,
            path=self.path,
            headers=self.headers
        )

        # todo: find appreciate router by path
        handler = [r for router in self.app.routers_collection for r in router.routers if r.path == '/hello']
        if handler:
            handler = handler.pop()
            handler.method = 'GET'
            response = self.get_handler(handler)(_request)
        else:
            return

        f = io.BytesIO(json.dumps(response).encode())
        f = io.BufferedReader(f)

        to_send = b"".join(headers)
        self.wfile.write(to_send)
        self.wfile.write(f.read())
        self.wfile.flush()  # actually send the response if not already done.

        self.log_request(200)

    def __send_response(self) -> None:
        return


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
