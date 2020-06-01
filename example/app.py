import os
import sys

from core.http_server import server

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.app import Toxic
from core.resource import Resource, APIRouter

router = APIRouter()


class MainResource(Resource):
    def get(self, request):
        return {'user': 'funnydman'}

    def post(self):
        raise {}


router.register('/hello', MainResource, name='my_first_router')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    server.run(app)
