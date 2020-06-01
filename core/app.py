from http.server import HTTPServer

from core.http_server import Server, HTTPRequestHandler


class BaseToxic(Server):
    def __init__(self):
        super().__init__(HTTPServer, HTTPRequestHandler)
        self.server = Server(self.server_class, self.handler_class)


class Toxic(BaseToxic):
    routers_collection = []

    def add_router(self, router):
        self.routers_collection.append(router)

    def run(self):
        self.server.serve()
