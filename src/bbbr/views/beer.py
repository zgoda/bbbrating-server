from flask import request

from ..models import Beer
from ..schema import beer_schema
from ..utils import get_pagination_params


def collection_get():
    page, limit = get_pagination_params(request)
    beers = Beer.select().order_by(Beer.name).paginate(page, limit)
    return {'beers': beer_schema.dump(beers, many=True)}
