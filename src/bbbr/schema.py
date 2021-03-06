from marshmallow import Schema, fields

fields.Field.default_error_messages.update({
    'required': 'To pole jest wymagane',
    'null': 'To pole nie może być puste',
    'validator_failed': 'Nieprawidłowa wartość',
})


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str()
    ratings = fields.Nested(
        'RatingSchema', only=['id', 'beer', 'date', 'overall'], many=True,
        dump_only=True,
    )
    is_active = fields.Bool(data_key='isActive')
    reg_date = fields.DateTime(data_key='regDate', dump_only=True)


user_schema = UserSchema()


class UserUpdateSchema(Schema):
    name = fields.Str()


user_update_schema = UserUpdateSchema()


class UserAuthSchema(Schema):
    email = fields.Email(
        required=True, error_messages={'invalid': 'Nieprawidłowy adres email'}
    )
    password = fields.Str(required=True)


user_login_schema = UserAuthSchema()


class RatingSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema, only=['id', 'name'], dump_only=True)
    beer = fields.Nested('BeerSchema', only=['id', 'name'], dump_only=True)
    colour = fields.Integer(required=True)
    colour_text = fields.Str(required=True, data_key='colourText')
    foam = fields.Integer(required=True)
    foam_text = fields.Str(required=True, data_key='foamText')
    aroma = fields.Integer(required=True)
    aroma_text = fields.Str(required=True, data_key='aromaText')
    taste = fields.Integer(required=True)
    taste_text = fields.Str(required=True, data_key='tasteText')
    carb = fields.Integer(required=True)
    carb_text = fields.Str(required=True, data_key='carbText')
    pack = fields.Integer(required=True)
    pack_text = fields.Str(required=True, data_key='packText')
    overall = fields.Integer(dump_only=True)
    package = fields.Str()
    rating = fields.Str()
    rating_html = fields.Str(dump_only=True, data_key='ratingHtml')


rating_schema = RatingSchema()


class BrewerySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    town = fields.Str(required=True)
    beers = fields.Nested('BeerSchema', only=['id', 'name'], many=True, dump_only=True)
    beers_brewed = fields.Nested(
        'BeerSchema', only=['id', 'name'], many=True, data_key='beersBrewed',
        dump_only=True,
    )
    is_active = fields.Boolean(data_key='isActive')
    is_contract = fields.Boolean(data_key='isContract')


brewery_schema = BrewerySchema()


class BeerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    brewery = fields.Nested(BrewerySchema, only=['id', 'name', 'town'], dump_only=True)
    brewed_at = fields.Nested(
        BrewerySchema, only=['id', 'name', 'town'], data_key='brewedAt', dump_only=True
    )
    ratings = fields.Nested(
        RatingSchema, only=['id', 'date', 'overall', 'user'], many=True, dump_only=True
    )
    is_active = fields.Boolean(data_key='isActive')


beer_schema = BeerSchema()
