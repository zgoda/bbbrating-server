from flask import Flask
from pony.flask import Pony

from .resource.user import user_collection


def make_app():
    app = Flask(__name__.split('.')[0])
    Pony(app)
    app.add_url_rule('/users', view_func=user_collection)
    return app
