from flask import request

from ..models import Brewery
from ..schema import brewery_schema
from ..utils import get_pagination_params


def collection_get():
    page, limit = get_pagination_params(request)
    breweries = Brewery.select().order_by(Brewery.name).paginate(page, limit)
    return {'breweries': brewery_schema.dump(breweries, many=True)}
