from flask.views import MethodView


class RatingCollection(MethodView):

    def get(self):
        return {'collection': 'ratings'}


rating_collection = RatingCollection.as_view('rating_collection')


class RatedBeerCollection(MethodView):

    def get(self):
        return {'collection': 'rated beers'}


rated_beer_collection = RatedBeerCollection.as_view('rated_beer_collection')
