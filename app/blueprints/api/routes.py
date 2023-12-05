from flask import request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from . import api

from app import db
from app.models import User, Address
from .auth import basic_auth, token_auth

basic_auth = HTTPBasicAuth()

@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}

#endpoint for all
@api.route('/users', methods=["GET"] ) 
def get_users():
    #users = db.session.execute(db.select(User)).scalars().all
    users = User.query.all()
    return [user.to_dict() for user in users]

#endpoint to get user by ID
@api.route('/users/<user_id>')
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return ['error' f'{user_id} not found']
    return user.to_dict()

#endpoint to add address
@api.route('/users', methods=["POST"])
@token_auth.login_required
def add_address():
    if not request.is_json:
        return {'error': 'must be application/json'}, 400
    #get data from request
    data = request.json
    #validate
    required_fields = ['first_name', 'last_name']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error' f"{ ', '.join(missing_fields)} must be in request"}, 400
    
    #get address data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    address = data.get('address')
    
    current_user = token_auth.current_user()

    #Create new address to add to DB
    new_address = Address(first_name=first_name, last_name=last_name, phone=phone, address=address)
    db.session.add(new_address)
    db.session.commit()
    return new_address.to_dict(), 201


@api.route('/address-list', methods=["POST"])
@token_auth.login_required
def list_address():
    if not request.is_json:
        return {'error': 'must be application/json'}, 400
    #get data from request
    data = request.json
    #validate
    required_fields = ['first_name', 'last_name']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error' f"{ ', '.join(missing_fields)} must be in request"}, 400
    
    #get address data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    address = data.get('address')
    
    current_user = token_auth.current_user()

    #Create new address to add to DB
    new_address = Address(first_name=first_name, last_name=last_name, phone=phone, address=address)
    db.session.add(new_address)
    db.session.commit()
    return new_address.to_dict(), 201