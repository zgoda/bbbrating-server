from flask import jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_required,
    set_refresh_cookies,
)
from marshmallow.exceptions import ValidationError
from peewee import IntegrityError
from werkzeug.exceptions import NotFound

from ..models import User
from ..schema import user_create_schema, user_schema, user_update_schema


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
        user_data = user_create_schema.load(request.json)
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
    return resp, 201, {'Location': url_for('user.item.get', email=user.email)}


@jwt_required
def item_get():
    user = User.get_or_none(User.email == get_jwt_identity())
    if user is None:
        raise NotFound()
    return user_schema.dump(user)


@jwt_required
def item_post():
    user = User.get_or_none(User.email == get_jwt_identity())
    if user is None:
        raise NotFound()
    try:
        user_data = user_update_schema.load(request.json)
    except ValidationError as e:
        return {'error': str(e)}, 400
    for k, v in user_data.items():
        setattr(user, k, v)
    user.save()
    return user_schema.dump(user)
