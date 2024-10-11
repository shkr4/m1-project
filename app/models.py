from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.Integer)
    role = db.Column(db.String)
    address = db.Column(db.Text)
    order = db.Column(db.PickleType)


class Professional(UserMixin, db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.Column(db.PickleType, db.ForeignKey('user.order'))
    services = db.Column(db.PickleType, db.ForeignKey('user.order'))
    YoE = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    pin = db.Column(db.Integer)


# user = User(name = name, password = password, email = email, YoE = YoE, services = service, UpFile = UpFile, pin = pin,
#     address = address)
