# routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    User.create_user(data['username'], data['password'])
    return jsonify(message='User registered'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_user(data['username'])
    if user and User.verify_password(user, data['password']):
        access_token = create_access_token(identity=user['username'])
        return jsonify(access_token=access_token)
    return jsonify(message='Invalid credentials'), 401
