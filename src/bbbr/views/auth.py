from flask import request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_refresh_token_required, get_raw_jwt
)

from ..models import User, RevokedToken
from ..schema import user_login_schema
from ..ext import jwt


@jwt.token_in_blacklist_loader
def check_token_blacklisted(decrypted_token: dict) -> bool:
    jti = decrypted_token['jti']
    return RevokedToken.is_blacklisted(jti)


def login():
    data = user_login_schema.load(request.json)
    user = User.get(email=data['email'])
    if user is not None and user.check_password(data['password']):
        resp = {
            'accessToken': create_access_token(identity=data['email']),
            'refreshToken': create_refresh_token(identity=data['email']),
        }
        return resp
    return {'error': 'User not found or wrong password'}, 404


@jwt_refresh_token_required
def refresh():
    email = get_jwt_identity()
    return {'accessToken': create_access_token(email)}


@jwt_refresh_token_required
def logout():
    jti = get_raw_jwt()['jti']
    RevokedToken(jti=jti)
    return ''
