import os
import sys

from toxic.core.app import Toxic
from toxic.core.responses import Response
from toxic.core.server.wsgi import my_wsgi

sys.path.append(os.getcwd())

from toxic.core.resource import Resource, APIRouter

router = APIRouter()

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


class SignInView(Resource):
    def post(self, request):
        data = request.data

        return Response({'signed': True})


class HomeView(Resource):
    def get(self):
        return {}


router.register('^/$', HomeView, name='index')
router.register('^/sign-in$', SignInView, name='sign-in')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    my_wsgi.run(app, host='', port=8000)
