import os

from flask import Flask
from pony.flask import Pony

from .ext import jwt
from .resource.user import user_collection, user_item


def make_app():
    app = Flask(__name__.split('.')[0])
    app.config['SECRET_KEY'] = app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
    configure_extensions(app)
    app.add_url_rule('/users', 'user.collection', view_func=user_collection)
    app.add_url_rule('/user/<int:user_id>', 'user.item', view_func=user_item)
    return app


def configure_extensions(app: Flask):
    Pony(app)
    jwt.init_app(app)
