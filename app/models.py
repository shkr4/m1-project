from . import db
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableDict


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.Integer)
    role = db.Column(db.String)
    address = db.Column(db.Text)
    status = db.Column(db.String)

    # The 'backref' creates a virtual column in the Order table linking back to User
    orders = db.relationship('Order', backref='user', lazy=True)


class Professionals(db.Model):
    __tablename__ = "professionals"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # FK to User
    business_name = db.Column(db.String)
    YoE = db.Column(db.Integer)
    address = db.Column(db.Text)
    pin = db.Column(db.Integer)
    status = db.Column(db.String)
    ServiceOffered = db.Column(MutableDict.as_mutable(db.PickleType))

    # 'backref' links Orders to Professionals
    orders = db.relationship('Order', backref='professional', lazy=True)

    # 'backref' links Services to Professionals
    services = db.relationship('Services', backref='professional', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey(
        'professionals.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float(precision=2, decimal_return_scale=2))

    # No need for explicit relationship definition here as 'backref' handles it


class Services(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String, nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)

    # FK to Professionals, pointing to `id` of the professionals table
    serviceProvider = db.Column(db.Integer, db.ForeignKey('professionals.id'))

    # 'backref' allows easy access to related professionals in the relationship


# user = User(name = name, password = password, email = email, YoE = YoE, services = service, UpFile = UpFile, pin = pin,
#     address = address)
