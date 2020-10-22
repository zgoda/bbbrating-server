from flask import jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_required,
    set_refresh_cookies,
)
from marshmallow.exceptions import ValidationError
from peewee import IntegrityError
from werkzeug.exceptions import Forbidden, NotFound

from ..models import User
from ..schema import UserCreateSchema, user_schema


@jwt_required
def collection_get():
    users = (
        User.select()
        .where(User.is_active)
        .order_by(User.email)
    )
    return {'users': user_schema.dump(users, many=True)}


def collection_post():
    try:
        user_data = UserCreateSchema().load(request.json)
    except ValidationError as e:
        return {'error': str(e)}, 400
    password = User.gen_password(user_data.pop('password'))
    try:
        user = User.create(password=password, **user_data)
    except IntegrityError:
        return {'error': 'Użytkownik o podanym adresie email już istnieje'}, 400
    resp = jsonify({
        'accessToken': create_access_token(identity=user_data['email']),
    })
    set_refresh_cookies(resp, create_refresh_token(identity=user_data['email']))
    return resp, 201, {'Location': url_for('user.item', email=user.email)}


@jwt_required
def item_get(email):
    user = User.get_or_none(User.email == email)
    if user is None:
        raise NotFound()
    if get_jwt_identity() != email:
        raise Forbidden()
    return user_schema.dump(user)
