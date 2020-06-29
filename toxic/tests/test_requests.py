import unittest

from toxic.core.server.http_server import HTTPServer


class TestRequest(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer()
        self.server.run('', port=9020)

    def test_multiple_requests(self):
        pass
