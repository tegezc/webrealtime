from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    hobby = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
