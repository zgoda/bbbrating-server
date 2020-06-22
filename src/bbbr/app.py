import falcon

from .models import DBSessionMiddleware
from .resource import user_collection


def make_app():
    app = falcon.API(middleware=[DBSessionMiddleware()])
    app.add_route('/user', user_collection)
    return app


app = make_app()
