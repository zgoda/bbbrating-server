import os
from datetime import datetime

import peewee
import icu
from markdown import markdown
from passlib.context import CryptContext
from peewee import (
    BooleanField, CharField, DateTimeField, ForeignKeyField, IntegerField, TextField,
)

collator = icu.Collator.createInstance(icu.Locale('pl_PL.utf-8'))

pwd_context = CryptContext(schemes=['bcrypt'])


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(stored: str, password: str) -> bool:
    return pwd_context.verify(password, stored)


DB_DRIVER_MAP = {
    'postgres': peewee.PostgresqlDatabase,
    'mysql': peewee.MySQLDatabase,
    'sqlite': peewee.SqliteDatabase,
}


def _get_db_driver_class():
    name = os.getenv('DB_DRIVER')
    if name is None:
        name = 'sqlite'
    name = name.lower()
    return DB_DRIVER_MAP[name]


db = _get_db_driver_class()(None)


@db.collation('PL')
def collate_pl(s1, s2):
    return collator.compare(s1, s2)


class Model(peewee.Model):
    class Meta:
        database = db


class User(Model):
    email = CharField(max_length=200, primary_key=True)
    name = CharField(max_length=100, null=True, collation='PL')
    password = TextField()
    is_active = BooleanField(default=True, index=True)
    reg_date = DateTimeField(default=datetime.utcnow, index=True)

    @staticmethod
    def gen_password(password: str) -> str:
        return generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Brewery(Model):
    name = CharField(max_length=200, collation='PL')
    town = CharField(max_length=200, collation='PL')
    is_active = BooleanField(default=True, index=True)
    is_contract = BooleanField(default=False)

    class Meta:
        indexes = (
            (('name', 'town'), True),
        )

    def __str__(self):
        return f'{self.name}, {self.town}'


class Beer(Model):
    name = CharField(max_length=200, index=True, collation='PL')
    brewery = ForeignKeyField(Brewery, backref='beers')
    brewed_at = ForeignKeyField(Brewery, backref='beers_brewed', null=True)
    is_active = BooleanField(default=True, index=True)

    def __str__(self):
        return f'{self.name} ({self.brewery.name})'


class RevokedToken(Model):
    jti = CharField(max_length=200, primary_key=True)
    exp = DateTimeField()

    @classmethod
    def is_blacklisted(cls, jti: str) -> bool:
        return bool(cls.get_or_none(jti=jti))


class Rating(Model):
    beer = ForeignKeyField(Beer, backref='ratings')
    date = DateTimeField(default=datetime.utcnow, index=True)
    colour = IntegerField()
    colour_text = TextField()
    foam = IntegerField()
    foam_text = TextField()
    aroma = IntegerField()
    aroma_text = TextField()
    taste = IntegerField()
    taste_text = TextField()
    carb = IntegerField()
    carb_text = TextField()
    pack = IntegerField()
    pack_text = TextField()
    overall = IntegerField()
    package = TextField(null=True)
    rating = TextField(null=True)
    rating_html = TextField(null=True)
    user = ForeignKeyField(User, backref='ratings', on_delete='SET NULL', null=True)

    def __str__(self):
        return f'{self.beer.name}'

    def calc_overall_rating(self) -> int:
        notes = [self.colour, self.foam, self.aroma, self.taste, self.carb, self.pack]
        return int(float(sum(notes)) / len(notes))

    def _recalc(self):
        self.overall = self.calc_overall_rating()
        if self.rating:
            self.rating_html = markdown(self.rating)


ALL_MODELS = [User, Brewery, Beer, RevokedToken, Rating]
