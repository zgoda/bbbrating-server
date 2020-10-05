from flask.views import MethodView


class RatingCollection(MethodView):

    def get(self):
        return {'collection': 'ratings'}


rating_collection = RatingCollection.as_view('rating_collection')
