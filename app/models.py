import os
from app import db, login
import base64
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    addresses = db.relationship('Address', backref='addresses')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password', ''))

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    def __repr__(self):
        return f"<Address {self.user_id}|{self.username}>"
    
    def get_id(self):
        return self.user_id
    
    def to_dict(self):
        return {
            'id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.addresses,
            'date_created' : self.date_created

        }
    

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __repr__(self):
        return f"<ADDRESS {self.id}|{self.address}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address,
            'Time' : self.date_created

        }
@login.user_loader
def get_user(user_id):
    return db.session.get(User, user_id)