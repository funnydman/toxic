import io
import re
from http.server import HTTPServer
from inspect import signature
from typing import Callable, Tuple

from toxic.constants import ContentType
from toxic.core import status
from toxic.core.exceptions import HTTPException
from toxic.core.request import Request
from toxic.core.resource import Router
from toxic.core.server.base_http import BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):
    _header_buffer = []

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def process_request(
            self,
            handler,
            method: str,
            params: dict,
            request: Request
    ) -> Callable:
        _handler = getattr(handler.handler_cls(), method.lower(), None)
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

    @staticmethod
    def process_form_urlencoded_data(data_str: bytes) -> dict:
        decoded = data_str.decode()
        res = [obj.split('=') for obj in decoded.split('&')]
        return dict(res)

    def handle_one_request(self):
        self._handle_one_request()
        data = {}

        if self.headers['Content-Type'] == ContentType.application_form_urlencoded:
            data = self.process_form_urlencoded_data(self.rfile.read())

        _request = Request(
            method=self.command,
            path=self.path,
            headers=self.headers,
            data=data
        )

        handler, params = self.find_handler_by_path(_request.path)

        response = self.process_request(handler, self.command, params, _request)

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

    def _send_response(self, response):
        self.send_begin_header(response.status_code)

        self.__send_header("Content-Type", response.content_type)

        self.__send_header('Server', self.version_string())
        self.__send_header('Date', self.date_time_string())
        self.__send_header('Content-Length', response.content_length)
        self.__end_headers()

        self.__send_data(response)

    def __send_data(self, response) -> None:

        f = io.BytesIO(response.render().encode())
        f = io.BufferedReader(f)

        self.wfile.write(f.read())

        self.wfile.flush()  # actually send the response if not already done.

        self.log_request(response.status_code)

    def __send_header(self, keyword: str, value: str) -> None:
        self._header_buffer.append(
            f"{keyword}: {value}\r\n".encode('latin-1', 'strict')
        )

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