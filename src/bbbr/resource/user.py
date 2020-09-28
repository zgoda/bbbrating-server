from flask import jsonify, request, url_for
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, set_refresh_cookies,
)
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound

from ..models import User, db
from ..schema import UserCreateSchema, user_schema


class UserCollection(MethodView):

    @jwt_required
    def get(self):
        users = User.select(lambda u: u.is_active is True)
        return {'users': user_schema.dump(users, many=True)}

    def post(self):
        try:
            user_data = UserCreateSchema().load(request.json)
        except ValidationError as e:
            return {'error': str(e)}, 400
        password = User.gen_password(user_data.pop('password'))
        user = User(password=password, **user_data)
        try:
            db.flush()
            resp = jsonify({
                'accessToken': create_access_token(identity=user_data['email']),
            })
            set_refresh_cookies(resp, create_refresh_token(identity=user_data['email']))
            return resp, 201, {'Location': url_for('user.item', email=user.email)}
        except Exception as e:
            db.rollback()
            return {'error': str(e)}, 400


user_collection = UserCollection.as_view('user_collection')


class UserItem(MethodView):

    @jwt_required
    def get(self, email: str):
        user = User.get(email=email)
        if user is None:
            raise NotFound()
        return user_schema.dump(user)


user_item = UserItem.as_view('user_item')
