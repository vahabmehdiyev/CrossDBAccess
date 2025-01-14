from api.auth.auth_action import AuthDAO

class AuthService:
    def __init__(self, dao: AuthDAO):
        self.auth_dao = dao

    def generate_csrf_token(self):
        return self.auth_dao.generate_csrf_token()

    def get_session(self):
        return self.auth_dao.get_session()

    def user_login(self, data, lang):
        return self.auth_dao.user_login(data, lang)

    def recovery_pass(self, data):
        return self.auth_dao.recovery_pass(data)

    def confirm_recovery_pass(self, token):
        return self.auth_dao.confirm_recovery_pass(token)

    def logout(self):
        return self.auth_dao.logout()

