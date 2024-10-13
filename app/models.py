from . import db
from flask_login import UserMixin


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
    order = db.Column(db.PickleType)


class Professionals(db.Model):
    __tablename__ = "professionals"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.Column(db.PickleType, db.ForeignKey('user.order'))
    services = db.Column(db.PickleType, db.ForeignKey('user.order'))
    YoE = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    pin = db.Column(db.Integer)


orders = db.Table('orders',
                  db.Column('user_id', db.Integer, db.ForeignKey(
                      'user.id'), primary_key=True),
                  db.Column('professional_id', db.Integer, db.ForeignKey(
                      'professionals.id'), primary_key=True),
                  db.Column('status', db.String),
                  db.Column('rating', db.Float))


class Services(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String)
    price = db.Column(db.Integer)
    provider = db.Column(db.String)


# user = User(name = name, password = password, email = email, YoE = YoE, services = service, UpFile = UpFile, pin = pin,
#     address = address)
