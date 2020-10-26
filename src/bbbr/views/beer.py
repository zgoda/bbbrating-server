from flask import request

from ..models import Beer
from ..schema import beer_schema


def collection_get():
    limit = request.args.get('limit')
    if limit is None:
        limit = 10
    limit = int(limit)
    page = int(request.args.get('page', '1'))
    beers = Beer.select().order_by(Beer.name).paginate(page, limit)
    return {'beers': beer_schema.dump(beers, many=True)}
