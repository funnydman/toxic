import os
import sys

from example.db.client import conn, queries
from toxic.core import server, Toxic, Response, status
from toxic.core.exceptions import HTTPException
from toxic.core.helpers import render_template

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toxic.core.resource import Resource, APIRouter

router = APIRouter()


class SignInView(Resource):
    def post(self, request):
        data = request.data
        # user = queries.find_user_by_username(conn, username=data['username'])
        # if user is None:
        #     raise HTTPException(detail='NO_SUCH_USER', status_code=status.HTTP_NOT_FOUND)

        return Response({})


class HomeView(Resource):
    def get(self):
        return render_template('index.html', {})


router.register('^/$', HomeView, name='index')
router.register('^/sign-in$', SignInView, name='sign-in')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    server.run(app)
