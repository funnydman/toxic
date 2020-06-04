import os
import sys

from example.db.client import conn, queries
from toxic.core import Response
from toxic.core import server, Toxic
from toxic.core.helpers import render_template

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toxic.core.resource import Resource, APIRouter

router = APIRouter()


class MainResource(Resource):
    def get(self, name):
        return Response({'user': name})

    def post(self):
        raise {}


class JsonHelloWorld(Resource):
    def get(self, name):
        return render_template('index.html', {'name': name})


class HomeView(Resource):
    def get(self):
        user = queries.find_user_by_username(conn, username='Dima')
        return Response({'user': user})


router.register('/', HomeView, name='index')
router.register('/hello/json/(?P<name>\w+)', MainResource, name='name_in_json')
router.register('/hello/html/(?P<name>\w+)', JsonHelloWorld, name='name_in_html')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    server.run(app)
