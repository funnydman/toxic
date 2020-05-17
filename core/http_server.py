import contextvars
import io
from http.server import HTTPServer, BaseHTTPRequestHandler

from core.request import Request

request = contextvars.ContextVar("request")


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        f = io.BytesIO(b"{\"name\": \"funnydman\"}")
        self.parse_request()
        _request = Request(
            method=self.command,
            path=self.path,
            headers=self.headers
        )
        request.set(_request)

        f = io.BufferedReader(f)
        headers = [
            b'HTTP/1.0 200 OK\r\n',
            b'Server: SimpleHTTP/0.6 Python/3.8.2\r\n',
            b'Date: Fri, 15 May 2020 20:18:36 GMT\r\n',
            b'Content-type: application/json; charset=utf-8\r\n',
            b'Content-Length: 200\r\n', b'\r\n'
        ]
        # todo: find out right handler or request

        to_send = b"".join(headers)
        self.wfile.write(to_send)
        self.wfile.write(f.read())
        self.log_request(200)

    def handle_one_request(self):
        print("Test")
        # super().handle_one_request()


class Server:
    def __init__(self, server_class, handler_class):
        self.server_class = server_class
        self.handler_class = handler_class

    def serve(self):
        server_address = ('', 8000)
        httpd = self.server_class(server_address, self.handler_class)
        httpd.serve_forever()


server = Server(HTTPServer, HTTPRequestHandler)

if __name__ == '__main__':
    server.serve()
