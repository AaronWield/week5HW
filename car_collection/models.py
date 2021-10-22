from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref='owner', lazy=True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200), nullable = True)
    type = db.Column(db.String(100), nullable = True)
    color = db.Column(db.String(50))
    year = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, type, color, year, make, model, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.type = type
        self.color = color
        self.year = year
        self.make = make
        self.model = model
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'type', 'color', 'year', 'make', 'model']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
