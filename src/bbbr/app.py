from flask import Flask
from pony.flask import Pony

from .ext import jwt
from .views import auth, brewery, user


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
    app.add_url_rule('/users', 'user.collection.get', user.collection_get)
    app.add_url_rule(
        '/users', 'user.collection.post', user.collection_post, methods=['POST']
    )
    app.add_url_rule('/user/<email>', 'user.item', user.item_get)
    app.add_url_rule('/login', 'auth.login', auth.login, methods=['POST'])
    app.add_url_rule('/token/refresh', 'auth.refresh', auth.refresh, methods=['POST'])
    app.add_url_rule('/logout', 'auth.logout', auth.logout, methods=['POST'])
    app.add_url_rule('/breweries', 'brewery.collection.get', brewery.collection_get)
