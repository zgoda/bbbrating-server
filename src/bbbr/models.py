import os
from datetime import datetime
from typing import Mapping, Union

from markdown import markdown
from pony.orm import Database, Optional, PrimaryKey, Required, Set
from werkzeug.security import check_password_hash, generate_password_hash


def db_params() -> Mapping[str, Union[str, int]]:
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
    email = PrimaryKey(str, 200)
    name = Optional(str, 100)
    password = Required(str)
    is_active = Required(bool, default=True)
    ratings = Set('Rating')

    @staticmethod
    def gen_password(password: str) -> str:
        return generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class RevokedToken(db.Entity):
    jti = PrimaryKey(str, 200)
    exp = Required(datetime)

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        return bool(cls.get(jti=jti))


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
    user = Optional(User)

    def calc_overall_rating(self) -> int:
        notes = [self.colour, self.foam, self.aroma, self.taste, self.carb, self.pack]
        return int(float(sum(notes)) / len(notes))

    def _recalc(self):
        self.overall = self.calc_overall_rating()
        if self.rating:
            self.rating_html = markdown(self.rating)

    def before_insert(self):
        self._recalc()

    def before_update(self):
        self._recalc()


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
