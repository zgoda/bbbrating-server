from ..models import Brewery, collate_pl
from ..schema import brewery_schema


def collection_get():
    breweries = Brewery.select().order_by(collate_pl.collation(Brewery.name))
    return {'breweries': brewery_schema.dump(breweries, many=True)}
