from flask import Flask
from pony.flask import Pony

from .ext import jwt
from .resource.user import user_collection, user_item
from .views.auth import login, logout, refresh


def make_app():
    app = Flask(__name__.split('.')[0])
    app.config.from_object('bbbr.config')
    configure_extensions(app)
    app.add_url_rule('/users', 'user.collection', view_func=user_collection)
    app.add_url_rule('/user/<int:user_id>', 'user.item', view_func=user_item)
    app.add_url_rule('/login', 'auth.login', login, methods=['POST'])
    app.add_url_rule('/token/refresh', 'auth.token.refresh', refresh, methods=['POST'])
    app.add_url_rule('/logout', 'auth.logout', logout, methods=['POST'])
    return app


def configure_extensions(app: Flask):
    Pony(app)
    jwt.init_app(app)
