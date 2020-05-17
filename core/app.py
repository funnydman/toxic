from core.http_server import server


class Toxic:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    routers_collection = []

    def add_router(self, router):
        self.routers_collection.append(router)

    def run(self):
        # run server
        server.serve()
