from flask import Flask
from pony.flask import Pony

from .resource.user import user_collection, user_item


def make_app():
    app = Flask(__name__.split('.')[0])
    Pony(app)
    app.add_url_rule('/users', 'user.collection', view_func=user_collection)
    app.add_url_rule('/user/<int:user_id>', 'user.item', view_func=user_item)
    return app
