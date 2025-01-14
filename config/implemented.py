from api.auth.auth_service import AuthService
from api.auth.auth_action import AuthDAO
from api.users.user_service import UsersService
from api.users.user_action import UsersDAO
from api.devices.devices_service import DevicesService
from api.devices.devices_action import DevicesDAO
from config.database import db

# Auth service
auth_service = AuthService(AuthDAO(db.session))

# Users service
users_service = UsersService(UsersDAO(db.session))

# Devices service
devices_service = DevicesService(DevicesDAO(db.session))
