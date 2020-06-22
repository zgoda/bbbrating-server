import falcon

from .resource import user_collection


def make_app():
    app = falcon.API()
    app.add_route('/user', user_collection)
    return app


app = make_app()
