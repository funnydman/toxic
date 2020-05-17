from core.app import Toxic
from core.resource import Resource, APIRouter

router = APIRouter()


class MainRouter(Resource):
    def get(self):
        # I need to have here request object
        return {'user': 'funnydman'}

    def post(self):
        raise NotImplementedError


router.register('/hello', MainRouter, name='my_first_router')

app = Toxic()
app.add_router(router)

if __name__ == '__main__':
    app.run()
