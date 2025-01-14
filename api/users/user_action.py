from flask import request
import jwt
from config.config import Config
from api.users.user_model import User

class UsersDAO:
    def __init__(self, session):
        self.session = session

    def get_user_info(self):
        try:
            bearer_token = request.headers.get('Authorization')
            if not bearer_token:
                return {'message': 'Authorization token is missing'}, 401

            try:
                decoded_token = jwt.decode(bearer_token, Config.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('sub').get('user_id')
            except jwt.ExpiredSignatureError:
                return {'message': 'Token has expired'}, 401
            except jwt.InvalidTokenError:
                return {'message': 'Invalid token'}, 401

            user = self.session.query(User).filter(User.id == user_id).first()

            if not user:
                return {'message': 'User not found'}, 404

            user_info = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "registration_date": user.registration_date.strftime('%Y-%m-%d'),
                "lang": user.lang
            }

            return user_info, 200

        except Exception as e:
            return {'message': f'Failed to retrieve user info: {str(e)}'}, 500
