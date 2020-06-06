from unittest import TestCase

from toxic.core.server.main import RequestHandler


class TestRequestParsing(TestCase):
    def test_decoding_request_string(self):
        request_string = b"GET / HTTP/1.1\r\n"
        parsed_request = RequestHandler._parse_request_line(request_string)

        self.assertEqual(parsed_request, "GET / HTTP/1.1")

    def test_is_http_version_valid(self):
        pass
