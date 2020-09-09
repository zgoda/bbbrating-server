from flask import jsonify
from flask.views import MethodView

from ..models import User
from ..schema import user_schema


class UserCollection(MethodView):

    def get(self):
        return jsonify({'users': user_schema.dump(User.select(), many=True)})


user_collection = UserCollection.as_view('user_collection')
