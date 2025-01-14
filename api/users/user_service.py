from api.users.user_action import UsersDAO

class UsersService:
    def __init__(self, dao: UsersDAO):
        self.users_dao = dao

    def get_user_info(self):
        return self.users_dao.get_user_info()
