class APIRouter:
    routers = []

    def register(self, path, handler_cls, **kwargs):
        self.routers.append((path, handler_cls))


class Resource:
    # need to get all methods of concrete class
    def __init__(self):
        pass

    def handle_GET(self):
        pass
