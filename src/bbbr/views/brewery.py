from ..models import Brewery
from ..schema import brewery_schema


def collection_get():
    breweries = Brewery.select().order_by(Brewery.name)
    return {'breweries': brewery_schema.dump(breweries, many=True)}
