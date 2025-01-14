from datetime import datetime
from config.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    lang = db.Column(db.String(5), default='en')
    is_auth = db.Column(db.Boolean, default=False)
    temporary_password = db.Column(db.String(255), nullable=True)
