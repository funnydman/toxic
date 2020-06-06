import os
import sys

from toxic.core.server.wsgi import run_with_wsgi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toxic.core import Toxic, Response
from toxic.core.helpers import render_template

from toxic.core.resource import Resource, APIRouter

router = APIRouter()

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


class SignInView(Resource):
    def post(self, request):
        data = request.data

        return Response({'signed': True})


class HomeView(Resource):
    def get(self):
        return render_template(os.path.join(TEMPLATE_DIR, 'index.html'), {})


router.register('^/$', HomeView, name='index')
router.register('^/sign-in$', SignInView, name='sign-in')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    run_with_wsgi(app)
