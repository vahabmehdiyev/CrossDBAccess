from config.implemented import users_service
from flask_restx import Resource, Namespace
from api.utils.utils import jwt_required

users_ns = Namespace('api/users')

@users_ns.route('/current/')
class UsersCurrentView(Resource):
    @jwt_required
    def get(self):
        user = users_service.get_user_info()
        return user

