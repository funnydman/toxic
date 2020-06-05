class Request:
    def __init__(self, *, method, path, headers, data=None):
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers
        self.data = data
