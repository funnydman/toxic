import io
from http.server import HTTPServer, SimpleHTTPRequestHandler


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        f = io.BytesIO(b"{\"name\": \"funnydman\"}")
        f = io.BufferedReader(f)
        headers = [
            b'HTTP/1.0 200 OK\r\n',
            b'Server: SimpleHTTP/0.6 Python/3.8.2\r\n',
            b'Date: Fri, 15 May 2020 20:18:36 GMT\r\n',
            b'Content-type: application/json; charset=utf-8\r\n',
            b'Content-Length: 200\r\n', b'\r\n'
        ]
        to_send = b"".join(headers)
        self.wfile.write(to_send)
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()


class Server:
    def __init__(self, server_class, handler_class):
        self.server_class = server_class
        self.handler_class = handler_class

    def serve(self):
        server_address = ('', 8000)
        httpd = self.server_class(server_address, self.handler_class)
        httpd.serve_forever()


Server(HTTPServer, HTTPRequestHandler).serve()
