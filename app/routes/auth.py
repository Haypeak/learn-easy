from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import mongo
from datetime import datetime
from app.models.user import create_user, check_user, update_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password', 'name']):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already registered'}), 400
        
    user = {
        'email': data['email'],
        'password': generate_password_hash(data['password']),
        'name': data['name'],
        'created_at': datetime.utcnow(),
        'role': 'student'
    }
    
    mongo.db.users.insert_one(user)
    
    # Remove password before sending response
    user.pop('password')
    token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'role': user['role']
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
        
    user = mongo.db.users.find_one({'email': data['email']})
    token = check_user(mongo, data['email'], data['password'])
    if token:    
        return jsonify({
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['full_name'],
                'role': user.get('role', 'student')
            }
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': current_user_id})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'id': str(user['_id']),
        'email': user['email'],
        'name': user['name'],
        'role': user.get('role', 'student')
    }), 200

# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
# from app import mongo
# from app.models.user import create_user, check_user, update_user

# auth_bp = Blueprint('auth_bp', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     create_user(mongo, data['email'], data['password'], data['fullName'])
#     return jsonify({"message": "User registered"}), 201

# @auth_bp.route('/update/<user_id>')
# def update_id(user_id):
#     data = request.get_json()
#     update_user(mongo, user_id, data['formYear'], data['subjects'], None, None, None, data['schoolName'], data['learning_goals'], data['educationLevel'])
#     return jsonify({"message": "User data updated"}), 200

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     token = check_user(mongo, data['email'], data['password'])
#     if token:
#         return jsonify({"token": token})
#     return jsonify({"error": "Invalid credentials"}), 401


# @auth_bp.route('/test', methods=['GET'])
# def test():
#     return jsonify({"message": "Test successful"})