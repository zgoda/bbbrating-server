import falcon
from falcon import Request, Response

from .models import User, db
from .schema import user_schema


class UserCollection:

    def on_get(self, req: Request, resp: Response):
        users = User.select().sort_by(User.name)
        resp.media = user_schema.dump(users, many=True)

    def on_post(self, req: Request, resp: Response):
        try:
            user = User(name=req.media['name'])
            db.flush()
            resp.status = falcon.HTTP_201
            resp.location = f'/user/{user.id}'
        except KeyError:
            resp.status = falcon.HTTP_400
            resp.media = {
                'error': 'User name not provided'
            }


user_collection = UserCollection()
