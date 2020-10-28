from flask import request
from peewee import JOIN, fn

from ..models import Beer, Rating
from ..schema import beer_schema
from ..utils import get_pagination_params


def collection_get():
    page, limit = get_pagination_params(request)
    beers = Beer.select().order_by(Beer.name).paginate(page, limit)
    return {'beers': beer_schema.dump(beers, many=True)}


def most_rated():
    count_ratings = fn.Count(Rating.id)
    beers = (
        Beer
        .select(Beer, count_ratings.alias('ratings_count'))
        .join(Rating, JOIN.INNER)
        .group_by(Beer)
        .order_by(count_ratings.desc())
        .limit(5)
    )
    return {'beers': beer_schema.dump(beers, many=True)}
