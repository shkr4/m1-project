from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    YoE = db.Column(db.Integer)
    #services = db.Column(db.PickleType)
    pin = db.Column(db.String)
    address = db.Column(db.Text)
    email = db.Column(db.String)


# user = User(name = name, password = password, email = email, YoE = YoE, services = service, UpFile = UpFile, pin = pin,
#     address = address)