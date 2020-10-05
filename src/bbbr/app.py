from flask import Flask
from pony.flask import Pony

from .ext import jwt
from .resource.rating import rating_collection
from .resource.user import user_collection, user_item
from .views import auth


def make_app() -> Flask:
    app = Flask(__name__.split('.')[0])
    app.config.from_object('bbbr.config')
    if app.debug:
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    configure_extensions(app)
    configure_routing(app)
    return app


def configure_extensions(app: Flask):
    Pony(app)
    jwt.init_app(app)


def configure_routing(app: Flask):
    app.add_url_rule('/users', 'user.collection', view_func=user_collection)
    app.add_url_rule('/user/<email>', 'user.item', view_func=user_item)
    app.add_url_rule('/ratings', 'rating_collection', view_func=rating_collection)
    app.add_url_rule('/login', 'auth.login', auth.login, methods=['POST'])
    app.add_url_rule('/token/refresh', 'auth.refresh', auth.refresh, methods=['POST'])
    app.add_url_rule('/logout', 'auth.logout', auth.logout, methods=['POST'])
