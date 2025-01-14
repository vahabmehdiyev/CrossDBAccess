from flask import Flask
from flask_restx import Api
from config.config import Config
from config.database import db
from flask_jwt_extended import JWTManager
from api.mail_manager import mail
from flask_login import LoginManager
from api.users.user_model import User
from flask_migrate import Migrate

# Namespaces
from api.auth.auth_view import auth_ns
from api.users.user_view import users_ns
from api.devices.devices_view import devices_ns

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Migrate
migrate = Migrate(app, db)

# Initialize Mail
mail.init_app(app)

# Initialize Database
db.init_app(app)
jwt = JWTManager(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register API namespaces
api = Api(app)
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(users_ns, path='/api/users')
api.add_namespace(devices_ns, path='/api/devices')

# Main application configuration
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(host="0.0.0.0", port=5000, debug=False)
