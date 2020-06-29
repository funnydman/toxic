import os
import selectors
import sys
import traceback
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
from typing import Tuple

from toxic.core.server.constants import METHOD_IS_NOT_SUPPORTED, HTTP_VERSION_IS_NOT_SUPPORTED
from toxic.core.server.request_handler import HTTPRequestHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from toxic.core.server.exceptions import BadRequestLine

allowed_http_methods = frozenset({'OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'})


class TCPServer:
    address_family = AF_INET
    type = SOCK_STREAM

    def __init__(self) -> None:
        """
        Notes:
            Socket must be in blocking mode to use makefile
        """
        self.socket = socket(family=self.address_family, type=self.type)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.sel = selectors.DefaultSelector()

    def __del__(self):
        self.close()

    def close(self) -> None:
        self.socket.close()

    def accept(self, sock, mask):
        conn, addr = self.socket.accept()
        self.wfile = conn.makefile('wb', buffering=0)
        self.rfile = conn.makefile('rb', buffering=0)

        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        with conn:
            try:
                self.handler(conn)
            finally:
                self.sel.unregister(conn)
                self.wfile.flush()
                self.wfile.close()
                self.rfile.close()

    def run(self, host: str, port: int) -> None:
        self.sel.register(self.socket, selectors.EVENT_READ, self.accept)

        self.socket.bind((host, port))
        self.socket.listen()
        while True:
            events = self.sel.select(timeout=0.2)
            for key, mask in events:
                try:
                    callback = key.data
                    callback(key.fileobj, mask)
                except Exception as e:
                    # middleware here
                    # do not close the connection just print the error message
                    traceback.print_exc()

    def handler(self, conn) -> None:
        pass


class HTTPServer(TCPServer):
    def __init__(self, handler_cls):
        super().__init__()
        self.handler_cls = handler_cls

    default_http_version = 'HTTP/1.1'
    max_request_uri_len = 8192  # 8KB
    max_bytes_to_read = 65535

    default_decoding = 'latin-1'

    def parse_request_line(self, raw_line: bytes) -> Tuple[str, str, str]:
        if len(raw_line) >= self.max_request_uri_len:
            raise BadRequestLine('Request-URI Too Long')
        if not raw_line.endswith(b'\r\n'):
            raise BadRequestLine('Request line must be followed by CRLF')

        request_line = raw_line.decode(self.default_decoding).strip('\r\n')

        method, request_uri, http_version = request_line.split(" ")
        if method not in allowed_http_methods:
            raise BadRequestLine(METHOD_IS_NOT_SUPPORTED.format(method))
        if http_version != self.default_http_version:
            raise BadRequestLine(HTTP_VERSION_IS_NOT_SUPPORTED.format(http_version))
        return method, request_uri, http_version

    def parse_headers(self, raw_headers: bytes) -> dict:
        headers: list = raw_headers.decode(self.default_decoding).splitlines()

        return dict([h.split(': ', 1) for h in headers])

    # mock
    def log_request(self, string):
        sys.stdout.write(string + '\n')

    def handler(self, conn):
        # call here  handler
        raw_request_line = self.rfile.readline()
        method, request_uri, http_version = self.parse_request_line(raw_request_line)

        method_handler = self.handler_cls(method, request_uri)

        result = method_handler()

        self.log_request(method + ' ' + request_uri)

        request_data = self.rfile.read(self.max_bytes_to_read)

        raw_headers, _, raw_data = request_data.rpartition(b'\r\n')

        self.headers = self.parse_headers(raw_headers)

        self.wfile.write(b'HTTP/1.1 200 OK\r\n\r\n')


if __name__ == '__main__':
    server = HTTPServer(handler_cls=HTTPRequestHandler)

    server.run(host='', port=9000)
