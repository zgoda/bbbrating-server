from datetime import datetime

from flask import Response, jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt,
    jwt_refresh_token_required, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies,
)
from marshmallow.exceptions import ValidationError

from ..ext import jwt
from ..models import RevokedToken, User
from ..schema import user_login_schema


@jwt.token_in_blacklist_loader
def check_token_blacklisted(decrypted_token: dict) -> bool:
    jti = decrypted_token['jti']
    return RevokedToken.is_blacklisted(jti)


def login():
    try:
        data = user_login_schema.load(request.json)
    except ValidationError as e:
        return {'error': str(e)}, 400
    user = User.get_or_none(User.email == data['email'])
    if user is not None and user.check_password(data['password']):
        access_token = create_access_token(identity=data['email'])
        resp = jsonify({
            'accessToken': access_token,
        })
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, create_refresh_token(identity=data['email']))
        return resp
    return {'error': 'Nie znaleziono użytkownika lub nieprawidłowe hasło'}, 401


@jwt_refresh_token_required
def refresh():
    email = get_jwt_identity()
    resp = jsonify({'accessToken': create_access_token(identity=email)})
    set_refresh_cookies(resp, create_refresh_token(identity=email))
    set_access_cookies(resp, create_access_token(identity=email))
    return resp


@jwt_refresh_token_required
def logout():
    jwt = get_raw_jwt()
    jti = jwt['jti']
    exp = datetime.fromtimestamp(jwt['exp'])
    RevokedToken.create(jti=jti, exp=exp)
    resp = Response(status=200, content_type='text/plain')
    unset_jwt_cookies(resp)
    return resp
