import os

from datetime import datetime
from pony.orm import Database, Optional, Required, Set


def db_params() -> dict:
    db_driver = os.getenv('DB_DRIVER', 'sqlite').lower()
    params = {
        'provider': db_driver
    }
    if db_driver == 'sqlite':
        db_filename = os.getenv('DB_FILENAME', ':memory:')
        params.update({
            'filename': db_filename,
            'create_db': True,
        })
    else:
        if db_driver not in ('postgres', 'mysql'):
            raise RuntimeError(f'unknown database provider {db_driver}')
        params['user'] = os.getenv('DB_USER')
        params['host'] = os.getenv('DB_HOST', '127.0.0.1')
        db_port = os.getenv('DB_PORT')
        if db_port is not None:
            params['port'] = int(db_port)
        db_name = os.environ['DB_NAME']
        if db_driver == 'postgres':
            key = 'dbname'
        else:
            key = 'db'
        params[key] = db_name
        db_password = os.getenv('DB_PASSWORD')
        if db_password:
            if db_driver == 'postgres':
                key = 'password'
            else:
                key = 'passwd'
            params[key] = db_password
    return params


db = Database()


class User(db.Entity):
    name = Required(str, index=True)
    ratings = Set('Rating')


class Rating(db.Entity):
    beer_id = Required(int, index=True)
    date = Required(datetime, default=datetime.utcnow, index=True)
    colour = Required(int)
    colour_text = Required(str)
    foam = Required(int)
    foam_text = Required(str)
    aroma = Required(int)
    aroma_text = Required(str)
    taste = Required(int)
    taste_text = Required(str)
    carb = Required(int)
    carb_text = Required(str)
    pack = Required(int)
    pack_text = Required(str)
    overall = Optional(int)
    package = Optional(str)
    rating = Optional(str)
    rating_html = Optional(str)
    user = Required(User)


db.bind(**db_params())
db.generate_mapping(create_tables=True)
