from unittest import TestCase

from toxic.core.server.http_server import HTTPServer


class TestRequestParsing(TestCase):
    def setUp(self) -> None:
        self.server = HTTPServer()

    def test_decoding_request_string(self):
        request_string = b"GET / HTTP/1.1\r\n"
        res = self.server.parse_request_line(request_string)
        self.assertTrue(isinstance(res, tuple))
        self.assertTrue(len(res) == 3)

        method, parsed_uri, http_version = res

        self.assertEqual(method, 'GET')
        self.assertEqual(parsed_uri, '/')
        self.assertEqual(http_version, 'HTTP/1.1')

    def test_unsupported_http_version(self):
        request_string = b"GET / HTTP/1.0\r\n"

        with self.assertRaises(Exception) as context:
            _, _, http_version = self.server.parse_request_line(request_string)
            self.assertEqual('is not supported', str(context.exception))

    def test_with_no_CRLF(self):
        request_string = b"GET / HTTP/1.1"

        res = self.server.parse_request_line(request_string)
        self.assertTrue(isinstance(res, tuple))
        self.assertTrue(len(res) == 3)

        method, parsed_uri, http_version = res

        self.assertEqual(method, 'GET')
        self.assertEqual(parsed_uri, '/')
        self.assertEqual(http_version, 'HTTP/1.1')


