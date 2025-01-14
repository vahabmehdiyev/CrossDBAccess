from flask_restx import Resource, Namespace
from config.implemented import auth_service
from flask import request, redirect
from api.utils.utils import csrf_protected, jwt_required

auth_ns = Namespace('api/auth')

@auth_ns.route('/csrf/')
class CsrfView(Resource):
    def get(self):
        return auth_service.generate_csrf_token()

@auth_ns.route('/session/')
class SessionView(Resource):
    @csrf_protected
    @jwt_required
    def get(self):
        return auth_service.get_session()

@auth_ns.route('/login/')
class UserLoginView(Resource):
    @csrf_protected
    def post(self):
        data = request.json
        lang = request.headers.get('Accept-Language', 'en')
        return auth_service.user_login(data, lang)

@auth_ns.route('/recovery_pass/')
class RecoveryPassView(Resource):
    @csrf_protected
    def post(self):
        data = request.json
        return auth_service.recovery_pass(data)

@auth_ns.route('/recovery_pass/<token>/')
class ConfirmRecoveryPassView(Resource):
    def get(self, token):
        auth_service.confirm_recovery_pass(token)
        frontend_url = f"{request.url_root}/auth/confirm_success"
        return redirect(frontend_url)

@auth_ns.route('/logout/')
class UserLogoutView(Resource):
    @csrf_protected
    @jwt_required
    def get(self):
        return auth_service.logout()