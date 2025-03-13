from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import mongo
from app.models.user import create_user, check_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    create_user(mongo, data['email'], data['password'], data['fullName'])
    return jsonify({"message": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = check_user(mongo, data['email'], data['password'])
    if token:
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test successful"})