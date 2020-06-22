import os
from datetime import datetime
from typing import Any

from falcon import Request, Response
from markdown import markdown
from pony.orm import Database, Optional, Required, Set, db_session


class DBSessionMiddleware:

    def process_request(self, req: Request, resp: Response):
        session = db_session()
        req.pony_session = session
        session.__enter__()

    def process_response(
                self, req: Request, resp: Response, resource: Any, success: bool
            ):
        session = getattr(req, 'pony_session', None)
        if session is not None:
            session.__exit__()


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
        return params
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

    def calc_overall_rating(self):
        notes = [self.colour, self.foam, self.aroma, self.taste, self.carb, self.pack]
        return int(float(sum(notes)) / len(notes))

    def before_insert(self):
        self.overall = self.calc_overall_rating()
        if self.rating:
            self.rating_html = markdown(self.rating)

    def before_update(self):
        self.overall = self.calc_overall_rating()
        if self.rating:
            self.rating_html = markdown(self.rating)


@db.on_connect(provider='sqlite')
def sqlite_conn_params(db, connection):
    cursor = connection.cursor()
    pragmas = [
        'journal_mode = wal',
        'cache_size = -64000',
        'foreign_keys = 1',
        'ignore_check_constraints = 0'
    ]
    for pragma in pragmas:
        sql = f'PRAGMA {pragma}'
        cursor.execute(sql)


db.bind(**db_params())
db.generate_mapping(create_tables=True)
