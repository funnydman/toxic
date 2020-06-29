import os
import sys

from toxic.core.server.http_server import HTTPServer, HTTPRequestHandler

enc, esc = sys.getfilesystemencoding(), 'surrogateescape'


class my_wsgi:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    headers_set = []
    headers_sent = []

    @classmethod
    def run(cls, application, host: str, port: int):
        self = cls(host, port)
        http_server = HTTPServer(handler_cls=HTTPRequestHandler)

        application.http_server = http_server
        application.http_server.run(host=host, port=port)

        self._run(application)

    def _run(self, application) -> None:

        environ = {k: self.unicode_to_wsgi(v) for k, v in os.environ.items()}

        environ['wsgi.input'] = sys.stdin.buffer
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True

        if environ.get('HTTPS', 'off') in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        else:
            environ['wsgi.url_scheme'] = 'http'

        result = application(environ, self.start_response)
        try:
            for data in result:
                if data:  # don't send headers until body appears
                    self.write(data)
            if not self.headers_sent:
                self.write('')  # send headers now if body was empty
        finally:
            pass
            # if hasattr(result, 'close'):
            #     result.close()  # what is close and how it should behave?

    def write(self, data):
        out = sys.stdout.buffer

        if not self.headers_set:
            raise AssertionError("write() before start_response()")

        elif not self.headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = self.headers_sent[:] = self.headers_set
            out.write(self.wsgi_to_bytes('Status: %s\r\n' % status))
            for header in response_headers:
                out.write(self.wsgi_to_bytes('%s: %s\r\n' % header))
            out.write(self.wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(self, status, response_headers, exc_info=None):
        if exc_info:
            try:
                if self.headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None  # avoid dangling circular ref
        elif self.headers_set:
            raise AssertionError("Headers already set!")

        self.headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here,
        # *after* the headers are set.  That way, if an error
        # occurs, start_response can only be re-called with
        # exc_info set.

        return self.write

    @staticmethod
    def unicode_to_wsgi(u):
        return u.encode(enc, esc).decode('iso-8859-1')

    @staticmethod
    def wsgi_to_bytes(s):
        return s.encode('iso-8859-1')
