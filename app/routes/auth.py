from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import mongo
from datetime import datetime
from pymongo import DESCENDING
from app.models.user import create_user, check_user, update_user
from bson import ObjectId  # Add this import at the top of the file if not already present

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
    user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'id': str(user['_id']),
        'email': user['email'],
        'name': user['full_name'],
        'role': user.get('role', 'student')
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    if not any(k in data for k in ['bio', 'name', 'email']):
        return jsonify({'error': 'No fields to update provided'}), 400

    update_fields = {}
    fields_to_update = ['bio', 'name', 'avatar', 'password', 'schoolName', 'learning_goals', 'educationLevel', 'formYear']
    for field in fields_to_update:
        if field in data:
            update_fields[field if field != 'name' else 'full_name'] = (
                generate_password_hash(data[field]) if field == 'password' else data[field]
            )
    if 'email' in data:
        if mongo.db.users.find_one({'email': data['email'], '_id': {'$ne': ObjectId(current_user_id)}}):
            return jsonify({'error': 'Email already in use'}), 400
        update_fields['email'] = data['email']

    # Update user in the database
    result = mongo.db.users.update_one(
        {'_id': ObjectId(current_user_id)},
        {'$set': update_fields}
    )

    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'Profile updated successfully'}), 200

@auth_bp.route('/enrolled-courses', methods=['GET'])
@jwt_required()
def get_enrolled_courses():
    current_user_id = get_jwt_identity()
    print(f"Current User ID: {current_user_id}")
    user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    print(user)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if 'enrolled_courses' not in user:
        return jsonify({'error': 'No enrolled courses found'}), 404
    
    enrolled_courses = user.get('enrolled_courses', [])
    courses = list(mongo.db.courses.find({'_id': {'$in': enrolled_courses}}))
    
    # Prepare the response with progress information
    result = []
    for course in courses:
        course_id = course['_id']
        
        # Get content items for this course
        content_items = list(mongo.db.course_content.find({
            'course_id': course_id  # Assuming content items have course_id field
        }).sort('order', 1))
        
        # If no content items found, try looking up by direct ID (handling potential schema inconsistency)
        if not content_items:
            content_items = list(mongo.db.course_content.find({
                '_id': course_id
            }).sort('order', 1))
        
        # Get progress records for this course
        progress_records = list(mongo.db.user_progress.find({
            'user_id': ObjectId(current_user_id),
            'course_id': course_id
        }))
        
        # Create a mapping of content_id to completion status
        completed_content = {}
        for record in progress_records:
            completed_content[str(record['content_id'])] = {
                'completed': record['completed'],
                'updated_at': record['updated_at']
            }
        
        # Calculate overall progress
        total_items = len(content_items)
        completed_items = sum(1 for record in progress_records if record.get('completed', False))
        overall_progress = (completed_items / total_items) * 100 if total_items > 0 else 0
        
        # Find the last activity timestamp
        last_activity = None
        if progress_records:
            # Sort by updated_at in descending order and get the first one
            last_progress = sorted(progress_records, key=lambda x: x['updated_at'], reverse=True)[0]
            last_activity = last_progress['updated_at']
        
        # Format content items with completion status
        formatted_content = []
        for item in content_items:
            content_id = str(item['_id'])
            completion_info = completed_content.get(content_id, {'completed': False, 'updated_at': None})
            
            formatted_content.append({
                'id': content_id,
                'title': item.get('title', ''),
                'type': item.get('type', ''),
                'completed': completion_info['completed'],
                'last_updated': completion_info['updated_at']
            })
        
        # Add course with progress to result
        result.append({
            'id': str(course['_id']),
            'title': course['title'],
            'description': course['description'],
            'level': course.get('level', 'Beginner'),
            'overallProgress': overall_progress,
            'contentItems': formatted_content,
            'lastActivity': last_activity
        })
    
    return jsonify(result), 200


@auth_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    current_user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    achievements = user.get('achievements', [])
    return jsonify({'achievements': achievements}), 200

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

@auth_bp.route('/update/<user_id>')
def update_id(user_id):
    data = request.get_json()
    update_user(mongo, user_id, data['formYear'], data['subjects'], None, None, None, data['schoolName'], data['learning_goals'], data['educationLevel'])
    return jsonify({"message": "User data updated"}), 200

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