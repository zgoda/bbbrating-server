import os

from flask import Flask
from pony.flask import Pony

from .ext import jwt
from .resource.user import user_collection, user_item


def make_app():
    app = Flask(__name__.split('.')[0])
    app.config['SECRET_KEY'] = app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    Pony(app)
    jwt.init_app(app)
    app.add_url_rule('/users', 'user.collection', view_func=user_collection)
    app.add_url_rule('/user/<int:user_id>', 'user.item', view_func=user_item)
    return app
