from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId
from datetime import datetime

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    try:
        courses = list(mongo.db.courses.find())
        return jsonify([{
            'id': str(course['_id']),
            'title': course['title'],
            'description': course['description'],
            'level': course.get('level', 'beginner'),
            'topics': course.get('topics', []),
            'created_at': course.get('created_at')
        } for course in courses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/course/<course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    try:
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        # Get course content
        content = list(mongo.db.course_content.find(
            {'course_id': ObjectId(course_id)}).sort('order', 1))
        
        return jsonify({
            'id': str(course['_id']),
            'title': course['title'],
            'description': course['description'],
            'level': course.get('level', 'beginner'),
            'topics': course.get('topics', []),
            'content': [{
                'id': str(item['_id']),
                'title': item['title'],
                'type': item['type'],
                'content': item['content'],
                'order': item['order']
            } for item in content]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/course/<course_id>/progress', methods=['POST'])
@jwt_required()
def update_progress(course_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'content_id' not in data or 'completed' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        progress = {
            'user_id': ObjectId(current_user_id),
            'course_id': ObjectId(course_id),
            'content_id': ObjectId(data['content_id']),
            'completed': data['completed'],
            'updated_at': datetime.utcnow()
        }
        
        # Upsert progress
        mongo.db.user_progress.update_one(
            {
                'user_id': progress['user_id'],
                'course_id': progress['course_id'],
                'content_id': progress['content_id']
            },
            {'$set': progress},
            upsert=True
        )
        
        return jsonify({'message': 'Progress updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/course/<course_id>/progress', methods=['GET'])
@jwt_required()
def get_progress(course_id):
    current_user_id = get_jwt_identity()
    try:
        progress = list(mongo.db.user_progress.find({
            'user_id': ObjectId(current_user_id),
            'course_id': ObjectId(course_id)
        }))
        
        return jsonify([{
            'content_id': str(item['content_id']),
            'completed': item['completed'],
            'updated_at': item['updated_at']
        } for item in progress]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson.objectid import ObjectId

learning_bp = Blueprint('learning_bp', __name__)

@learning_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return jsonify({"progress": user.get("progress", [])})

@learning_bp.route('/update-progress', methods=['POST'])
@jwt_required()
def update_progress():
    data = request.get_json()
    user_id = get_jwt_identity()
    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"progress": {"topic": data['topic'], "score": data['score']}}}
    )
    return jsonify({"message": "Progress updated"})
