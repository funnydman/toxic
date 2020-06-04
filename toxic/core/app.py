from http.server import HTTPServer
from typing import List

from toxic.core.http_server import Server, HTTPRequestHandler
from toxic.core.resource import APIRouter


class BaseToxic(Server):
    def __init__(self) -> None:
        super().__init__(HTTPServer, HTTPRequestHandler)
        self.server = Server(self.server_class, self.handler_class)


class Toxic(BaseToxic):
    def __init__(self):
        super().__init__()

    routers_collection: List[APIRouter] = []

    def add_router(self, router: APIRouter) -> None:
        self.routers_collection.append(router)
