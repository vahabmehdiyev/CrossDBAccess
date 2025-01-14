from config.database import db

class CategoryType(db.Model):
    __tablename__ = 'category_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('category_types.id'))
    type = db.relationship('CategoryType')

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    serial_number = db.Column(db.String, unique=True)

class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), nullable=False, unique=True)
    item = db.Column(db.Integer, db.ForeignKey('items.id'))
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category_type = db.Column(db.Integer, db.ForeignKey('category_types.id'))
    user_id = db.Column(db.Integer, nullable=False)

class DeviceRemote(db.Model):
    __tablename__ = 'devices_remote'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), nullable=False, unique=True)
