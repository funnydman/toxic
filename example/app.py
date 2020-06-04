import os
import sys

from toxic.core import Response
from toxic.core import server, Toxic
from toxic.core.responses import HTMLResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toxic.core.resource import Resource, APIRouter

router = APIRouter()


def render_template(path_to_file: str, params):
    start_bracket = '{'
    end_bracket = '}'
    with open(path_to_file, 'r') as file:
        content = file.read()
    content = content.replace(f'{start_bracket}username{end_bracket}', params['name'])
    return HTMLResponse(content)


class MainResource(Resource):
    def get(self, request, name):
        return Response({'user': name})

    def post(self):
        raise {}


class JsonHelloWorld(Resource):
    def get(self, name):
        return render_template('../index.html', {'name': name})


router.register('/hello/json/(?P<name>\w+)', MainResource, name='my_first_router')
router.register('/hello/html/(?P<name>\w+)', JsonHelloWorld, name='my_first_router')

app = Toxic()

app.add_router(router)

if __name__ == '__main__':
    server.run(app)
