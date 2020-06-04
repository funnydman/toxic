from toxic.core.exceptions import ResourceNameMustBeUniqueError


class Router:
    def __init__(self, path, handler_cls, name) -> None:
        self.path = path
        self.handler_cls = handler_cls
        self.name = name


class APIRouter:
    routers = []
    registered_names = set()

    def register(self, path: str, handler_cls, name: str):
        if name in self.registered_names:
            raise ResourceNameMustBeUniqueError()
        self.routers.append(
            Router(path, handler_cls, name)
        )
        self.registered_names.add(name)


class Resource:
    # need to get all methods of concrete class
    def __init__(self):
        pass
