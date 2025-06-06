# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import mongo
# from bson import ObjectId

# user_bp = Blueprint('user', __name__)

# @user_bp.route('/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     current_user_id = get_jwt_identity()
#     try:
#         user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
#         if not user:
#             return jsonify({'error': 'User not found'}), 404
        
#         return jsonify({
#             'id': str(user['_id']),
#             'email': user['email'],
#             'name': user['name'],
#             'role': user.get('role', 'student'),
#             'created_at': user.get('created_at')
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @user_bp.route('/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user_id = get_jwt_identity()
#     data = request.get_json()
    
#     # Fields that are allowed to be updated
#     allowed_updates = ['name', 'email']
#     update_data = {k: v for k, v in data.items() if k in allowed_updates}
    
#     if not update_data:
#         return jsonify({'error': 'No valid fields to update'}), 400
        
#     try:
#         # Check if email is being updated and if it's already taken
#         if 'email' in update_data:
#             existing_user = mongo.db.users.find_one({
#                 'email': update_data['email'],
#                 '_id': {'$ne': ObjectId(current_user_id)}
#             })
#             if existing_user:
#                 return jsonify({'error': 'Email already in use'}), 400
        
#         # Update the user profile
#         result = mongo.db.users.update_one(
#             {'_id': ObjectId(current_user_id)},
#             {'$set': update_data}
#         )
        
#         if result.modified_count == 0:
#             return jsonify({'error': 'User not found or no changes made'}), 404
            
#         # Get updated user data
#         updated_user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
        
#         return jsonify({
#             'message': 'Profile updated successfully',
#             'user': {
#                 'id': str(updated_user['_id']),
#                 'email': updated_user['email'],
#                 'name': updated_user['name'],
#                 'role': updated_user.get('role', 'student')
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

from flask import Blueprint, jsonify, request
from app import mongo
from bson import ObjectId

from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint('user_bp', __name__)



@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Prepare the response
    response = {
        "metrics": [
            {"title": "Progress", "value": "75% Complete", "icon": "📘"},
            {"title": "Courses", "value": "4 Active", "icon": "📘"},
            {"title": "Goals", "value": "2 Achieved", "icon": "🎯"},
            {"title": "Awards", "value": "3 Earned", "icon": "🏆"}
        ],
        "tasks": user.get("tasks", []),
        "progress": user.get("learning_progress", [])
    }

    return jsonify(response)

@user_bp.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    data = request.get_json()

    # Validate the incoming data
    required_fields = ['fullName', 'email', 'phoneNumber', 'schoolName', 'educationLevel', 'formYear', 'learningGoals', 'subjects']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Update the user's profile in the database
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'full_name': data['fullName'],
            'email': data['email'],
            'phone_number': data['phoneNumber'],
            'school_name': data['schoolName'],
            'education_level': data['educationLevel'],
            'form_year': data['formYear'],
            'learning_goals': data['learningGoals'],
            'subjects': data['subjects'],
        }}
    )

    return jsonify({'message': 'Profile updated successfully'}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Prepare the response
    response = {
        "fullName": user.get("full_name"),
        "email": user.get("email"),
        "phoneNumber": user.get("phone_number"),
        "schoolName": user.get("school_name"),
        "educationLevel": user.get("education_level"),
        "formYear": user.get("form_year"),
        "learningGoals": user.get("learning_goals"),
        "subjects": user.get("subjects"),
    }

    return jsonify(response), 200