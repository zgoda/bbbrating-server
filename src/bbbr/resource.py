from falcon import Request, Response
from pony.orm import db_session

from .models import User
from .schema import user_schema


class UserCollection:

    @db_session
    def on_get(self, req: Request, resp: Response):
        users = User.select().sort_by(User.name)
        resp.media = user_schema.dump(users, many=True)


user_collection = UserCollection()
