class Router:
    def __init__(self, path, handler_cls, name) -> None:
        self.path = path
        self.handler_cls = handler_cls
        self.name = name


class APIRouter:
    routers = []

    def register(self, path, handler_cls, name):
        self.routers.append(Router(path, handler_cls, name))


class Resource:
    # need to get all methods of concrete class
    def __init__(self):
        pass
