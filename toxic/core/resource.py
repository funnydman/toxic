from toxic.core.exceptions import ResourceNameMustBeUniqueError


class Router:
    def __init__(self, path, handler_cls, name) -> None:
        self.path = path
        self.handler_cls = handler_cls
        self.name = name


class APIRouter:
    routers = []
    _registered_names = set()

    def register(self, path: str, handler_cls, name: str) -> None:
        if name in self._registered_names:
            raise ResourceNameMustBeUniqueError()
        self.routers.append(
            Router(path, handler_cls, name)
        )
        self._registered_names.add(name)


class Resource:
    def __init__(self):
        pass
