from typing import List

from toxic.core.resource import APIRouter


class Toxic:

    def __init__(self, version: str = None) -> None:
        self.version = version

    def __call__(self, environ: dict, start_response) -> List[bytes]:
        self.environ = environ
        self.start_response = start_response

        status = '200 OK'
        response_headers = [('Content-type', 'text/plain'), ('Accept', '*')]
        start_response(status, response_headers)
        return [b'Hello world\n']

    def dispatch(self):
        pass

    routers_collection: List[APIRouter] = []

    def add_router(self, router: APIRouter) -> None:
        self.routers_collection.append(router)
