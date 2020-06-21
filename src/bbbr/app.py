import falcon


def make_app():
    app = falcon.API()
    return app


app = make_app()
