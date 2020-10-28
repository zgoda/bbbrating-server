from ..models import Rating
from ..schema import rating_schema


def latest():
    ratings = Rating.select().order_by(Rating.date.desc()).limit(5)
    return {'ratings': rating_schema.dump(ratings, many=True)}
