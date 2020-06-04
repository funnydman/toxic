class ResourceNameMustBeUniqueError(Exception):
    pass


class HTTPException(Exception):
    def __init__(self, detail: str, status_code=500):
        self.detail = detail
        self.status_code = status_code
