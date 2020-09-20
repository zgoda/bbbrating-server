from marshmallow import Schema, fields


class UserSchema(Schema):
    ratings = fields.Nested(
        'RatingSchema', only=['id', 'beer_id', 'date', 'overall'], many=True
    )
    is_active = fields.Bool(data_key='isActive')

    class Meta:
        additional = ('email', 'name')


user_schema = UserSchema()


class UserAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


user_login_schema = UserAuthSchema()


class UserCreateSchema(UserAuthSchema):
    name = fields.Str(default='')


class RatingSchema(Schema):
    user = fields.Nested(UserSchema, only=['email', 'name'])
    beer_id = fields.Int(data_key='beerId')
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
