class Request:
    def __init__(
            self,
            *,
            method: str,
            path: str,
            headers: dict,
            data=None
    ):
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers
