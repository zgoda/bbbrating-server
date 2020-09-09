from flask import Response, jsonify, request
from flask.views import MethodView

from ..models import User, db
from ..schema import UserCreateSchema, user_schema


class UserCollection(MethodView):

    def get(self):
        return jsonify({'users': user_schema.dump(User.select(), many=True)})

    def post(self):
        sc = UserCreateSchema()
        user_data = sc.load(request.json)
        User(
            name=user_data['name'], email=user_data['email'],
            password=User.gen_password(user_data['password']),
        )
        db.flush()
        return Response(status=201)


user_collection = UserCollection.as_view('user_collection')
