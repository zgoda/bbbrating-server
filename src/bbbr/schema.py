from marshmallow import Schema, fields


class UserSchema(Schema):
    ratings = fields.Nested(
        'RatingSchema', only=['id', 'beer_id', 'date', 'overall'], many=True
    )

    class Meta:
        additional = ('id', 'email', 'name')


user_schema = UserSchema()


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str()
    password = fields.Str(required=True)


class RatingSchema(Schema):
    user = fields.Nested(UserSchema, only=['id', 'email', 'name'])

    class Meta:
        additional = (
            'id', 'beer_id', 'date', 'colour', 'colour_text', 'foam', 'foam_text',
            'aroma', 'aroma_text', 'taste', 'taste_text', 'carb', 'carb_text',
            'pack', 'pack_text', 'overall', 'package', 'rating', 'rating_html'
        )


rating_schema = RatingSchema()
