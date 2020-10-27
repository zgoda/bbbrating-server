import os
import tempfile

from flask import Flask

from .ext import jwt
from .models import ALL_MODELS, db
from .views import auth, beer, brewery, user


def make_app() -> Flask:
    app = Flask(__name__.split('.')[0])
    app.config.from_object('bbbr.config')
    configure_database(app)
    configure_hooks(app)
    configure_extensions(app)
    configure_routing(app)
    return app


def configure_database(app: Flask):
    driver = os.getenv('DB_DRIVER', 'sqlite')
    if app.testing:
        tmp_dir = tempfile.mkdtemp()
        db_name = os.path.join(tmp_dir, 'bbbr.db')
    else:
        db_name = os.getenv('DB_FILENAME')
    if driver == 'sqlite':
        kw = {
            'pragmas': {
                'journal_mode': 'wal',
                'cache_size': -1 * 64000,
                'foreign_keys': 1,
                'ignore_check_constraints': 0,
                'synchronous': 0,
            }
        }
        if db_name is None:
            db_name = ':memory:'
            kw = {}
    else:
        kw = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
    db.init(db_name, **kw)
    db.create_tables(ALL_MODELS)


def configure_hooks(app: Flask):
    @app.before_request
    def db_connect():
        db.connect(reuse_if_open=True)

    @app.teardown_request
    def db_close(exc):
        if not db.is_closed():
            db.close()


def configure_extensions(app: Flask):
    jwt.init_app(app)


def configure_routing(app: Flask):
    app.add_url_rule('/users', 'user.collection.get', user.collection_get)
    app.add_url_rule(
        '/users', 'user.collection.post', user.collection_post, methods=['POST']
    )
    app.add_url_rule('/user/<email>', 'user.item.get', user.item_get)
    app.add_url_rule(
        '/user/<email>', 'user.item.post', user.item_post, methods=['POST']
    )
    app.add_url_rule('/login', 'auth.login', auth.login, methods=['POST'])
    app.add_url_rule('/token/refresh', 'auth.refresh', auth.refresh, methods=['POST'])
    app.add_url_rule('/logout', 'auth.logout', auth.logout, methods=['POST'])
    app.add_url_rule('/breweries', 'brewery.collection.get', brewery.collection_get)
    app.add_url_rule('/beers', 'beer.collection.get', beer.collection_get)
