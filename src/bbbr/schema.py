from marshmallow import Schema, fields

fields.Field.default_error_messages.update({
    'required': 'To pole jest wymagane',
    'null': 'To pole nie może być puste',
    'validator_failed': 'Nieprawidłowa wartość',
})


class UserSchema(Schema):
    ratings = fields.Nested(
        'RatingSchema', only=['id', 'beer', 'date', 'overall'], many=True
    )
    is_active = fields.Bool(data_key='isActive')
    reg_date = fields.DateTime(data_key='regDate')

    class Meta:
        additional = ('email', 'name')


user_schema = UserSchema()


class UserAuthSchema(Schema):
    email = fields.Email(
        required=True, error_messages={'invalid': 'Nieprawidłowy adres email'}
    )
    password = fields.Str(required=True)


user_login_schema = UserAuthSchema()


class UserCreateSchema(UserAuthSchema):
    name = fields.Str(default='')


class RatingSchema(Schema):
    user = fields.Nested(UserSchema, only=['email', 'name'])
    beer = fields.Nested('BeerSchema', only=['id', 'name'])
    colour_text = fields.Str(data_key='colourText')
    foam_text = fields.Str(data_key='foamText')
    aroma_text = fields.Str(data_key='aromaText')
    taste_text = fields.Str(data_key='tasteText')
    carb_text = fields.Str(data_key='carbText')
    pack_text = fields.Str(data_key='packText')
    rating_html = fields.Str(data_key='ratingHtml')

    class Meta:
        additional = (
            'id', 'date', 'colour', 'foam', 'aroma', 'taste', 'carb', 'pack',
            'overall', 'package', 'rating',
        )


rating_schema = RatingSchema()


class BrewerySchema(Schema):
    name = fields.Str(required=True)
    town = fields.Str(required=True)
    beers = fields.Nested('BeerSchema', only=['id', 'name'], many=True)
    beers_brewed = fields.Nested(
        'BeerSchema', only=['id', 'name'], many=True, data_key='beersBrewed'
    )
    is_active = fields.Boolean(data_key='isActive')
    is_contract = fields.Boolean(data_key='isContract')

    class Meta:
        additional = ['id']


brewery_schema = BrewerySchema()


class BeerSchema(Schema):
    name = fields.Str(required=True)
    brewery = fields.Nested(BrewerySchema, only=['id', 'name', 'town'])
    brewed_at = fields.Nested(
        BrewerySchema, only=['id', 'name', 'town'], data_key='brewedAt'
    )
    ratings = fields.Nested(
        RatingSchema, only=['id', 'date', 'overall', 'user'], many=True
    )
    is_active = fields.Boolean(data_key='isActive')

    class Meta:
        additional = ['id']


beer_schema = BeerSchema()
