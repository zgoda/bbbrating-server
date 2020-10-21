from ..models import Beer
from ..schema import beer_schema


def collection_get():
    beers = Beer.select().order_by(Beer.name)
    return {'beers': beer_schema.dump(beers, many=True)}
