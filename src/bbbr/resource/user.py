from flask import Response, jsonify, request, url_for
from flask.views import MethodView

from ..models import User, db
from ..schema import UserCreateSchema, user_schema


class UserCollection(MethodView):

    def get(self):
        users = User.select(lambda u: u.is_active is True)
        return jsonify({'users': user_schema.dump(users, many=True)})

    def post(self):
        sc = UserCreateSchema()
        user_data = sc.load(request.json)
        user = User(
            name=user_data.get('name', ''), email=user_data['email'],
            password=User.gen_password(user_data['password']),
        )
        db.flush()
        return Response(
            status=201, headers={'Location': url_for('user.item', user_id=user.id)}
        )


user_collection = UserCollection.as_view('user_collection')


class UserItem(MethodView):

    def get(self, user_id: int):
        user = User.get(id=user_id)
        return jsonify(user_schema.dump(user))


user_item = UserItem.as_view('user_item')
