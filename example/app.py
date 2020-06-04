import os
import sys

from toxic.core import server, Toxic
from toxic.core.helpers import render_template

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toxic.core.resource import Resource, APIRouter

router = APIRouter()


class SignInView(Resource):
    def post(self, request):
        pass


class HomeView(Resource):
    def get(self):
        # user = queries.find_user_by_username(conn, username='Dima')
        return render_template('index.html', {})


router.register('^/$', HomeView, name='index')
router.register('/sign-in', SignInView, name='sign-in')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    server.run(app)
