from typing import List

from toxic.core.resource import APIRouter


class Toxic:
    def __init__(self, version: str = None):
        self.version = version

    def __call__(self, environ: dict, start_response: StartResponse) -> None:
        self.environ = environ
        self.start_response = start_response

    routers_collection: List[APIRouter] = []

    def add_router(self, router: APIRouter) -> None:
        self.routers_collection.append(router)
