from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId
from datetime import datetime
import openai

AIclient = openai.OpenAI(api_key='1b54a87aa050f5fc48571783d2d3692e4638a23e')

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
        course_obj_id = ObjectId(course_id)
        course = mongo.db.courses.find_one({'_id': course_obj_id})
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        # Get course content
        content_items = list(mongo.db.course_content.find(
            {'course_id': course_obj_id}).sort('order', 1))
        
        # If no content found with course_id field, try legacy query with _id field
        # This handles potential schema inconsistency
        if not content_items:
            content_items = list(mongo.db.course_content.find(
                {'_id': course_obj_id}).sort('order', 1))
        
        # Process content for frontend rendering
        processed_content = ""
        content_structure = []
        
        # Create HTML content and structure information from content items
        for item in content_items:
            if item.get('type') == 'text':
                processed_content += f"<div>{item.get('content', '')}</div>"
            elif item.get('type') == 'video':
                processed_content += f"<div class='video-container'><iframe src='{item.get('content', '')}' frameborder='0' allowfullscreen></iframe></div>"
            elif item.get('type') == 'image':
                processed_content += f"<div><img src='{item.get('content', '')}' alt='{item.get('title', 'Course image')}' /></div>"
            
            # Add to structure if it's a section
            if item.get('is_section', False):
                section = {
                    'title': item.get('title', 'Untitled Section'),
                    'description': item.get('description', ''),
                    'quizzes': []
                }
                
                # If this section has quizzes, add them
                quizzes = item.get('quizzes', [])
                if quizzes:
                    for quiz in quizzes:
                        section['quizzes'].append({
                            'id': str(quiz.get('_id', '')),
                            'title': quiz.get('title', 'Untitled Quiz')
                        })
                
                content_structure.append(section)
        
        # Return complete course data
        return jsonify({
            'id': str(course['_id']),
            'title': course['title'],
            'description': course['description'],
            'author': course.get('author', 'Unknown Author'),
            'level': course.get('level', 'beginner'),
            'topics': course.get('topics', []),
            'content': processed_content,
            'structure': {
                'sections': content_structure
            },
            'contentItems': [{
                'id': str(item['_id']),
                'title': item.get('title', ''),
                'type': item.get('type', ''),
                'content': item.get('content', ''),
                'order': item.get('order', 0)
            } for item in content_items]
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

@learning_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_user_progress():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return jsonify({"progress": user.get("progress", [])})

@learning_bp.route('/update-progress', methods=['POST'])
@jwt_required()
def update_user_progress():
    data = request.get_json()
    user_id = get_jwt_identity()
    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"progress": {"topic": data['topic'], "score": data['score']}}}
    )
    return jsonify({"message": "Progress updated"})

@learning_bp.route('/course/<course_id>/enrollment', methods=['POST'])
@jwt_required()
def enroll_in_course(course_id):
    current_user_id = get_jwt_identity()
    try:
        # Check if the course exists
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        # Add the course to the user's enrolled_courses
        mongo.db.users.update_one(
            {'_id': ObjectId(current_user_id)},
            {'$addToSet': {'enrolled_courses': ObjectId(course_id)}}
        )
        return jsonify({'message': 'Enrolled in course successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@learning_bp.route('/course/<course_id>/enrollment', methods=['GET'])
@jwt_required()
def get_enrollment_status(course_id):
    current_user_id = get_jwt_identity()
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
        is_enrolled = ObjectId(course_id) in user.get('enrolled_courses', [])
        progress = 0

        if is_enrolled:
            progress_records = mongo.db.user_progress.find({
                'user_id': ObjectId(current_user_id),
                'course_id': ObjectId(course_id)
            })
            completed_items = sum(1 for record in progress_records if record.get('completed', False))
            total_items = mongo.db.course_content.count_documents({'_id': ObjectId(course_id)})
            progress = (completed_items / total_items) * 100 if total_items > 0 else 0

        return jsonify({'isEnrolled': is_enrolled, 'progress': progress}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@learning_bp.route('/course/<course_id>/enrollment', methods=['DELETE'])
@jwt_required()
def unenroll_from_course(course_id):
    current_user_id = get_jwt_identity()
    try:
        # Remove the course from the user's enrolled_courses
        mongo.db.users.update_one(
            {'_id': ObjectId(current_user_id)},
            {'$pull': {'enrolled_courses': ObjectId(course_id)}}
        )
        # Optionally, remove progress records for the course
        mongo.db.user_progress.delete_many({
            'user_id': ObjectId(current_user_id),
            'course_id': ObjectId(course_id)
        })
        return jsonify({'message': 'Unenrolled from course successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Development/Testing route - not for production use
@learning_bp.route('/create-test-course', methods=['GET'])
def create_test_course():
    """Create a test course with content and structure for development/testing purposes."""
    try:
        # 1. Create the main course document
        course = {
            'title': 'Introduction to Python Programming',
            'description': 'A comprehensive introduction to Python programming language covering basics to advanced concepts.',
            'author': 'John Doe',
            'level': 'Beginner',
            'topics': ['Programming', 'Python', 'Computer Science'],
            'created_at': datetime.utcnow()
        }
        
        course_id = mongo.db.courses.insert_one(course).inserted_id
        
        # 2. Create course content items with different types
        content_items = [
            # Section 1: Introduction
            {
                'course_id': course_id,
                'title': 'Getting Started with Python',
                'type': 'text',
                'content': '<h3>Welcome to Python!</h3><p>Python is a high-level, interpreted programming language that is easy to learn and powerful to use.</p>',
                'order': 1,
                'is_section': True,
                'description': 'Introduction to the Python programming language',
                'quizzes': [
                    {
                        'title': 'Python Basics Quiz',
                        'description': 'Test your knowledge of Python basics'
                    }
                ]
            },
            {
                'course_id': course_id,
                'title': 'Installing Python',
                'type': 'text',
                'content': '<p>To get started with Python, you first need to install it on your computer. Visit <a href="https://python.org">python.org</a> to download the latest version.</p>',
                'order': 2
            },
            {
                'course_id': course_id,
                'title': 'Python Installation Demo',
                'type': 'video',
                'content': 'https://www.youtube.com/embed/YYXdXT2l-Gg',
                'order': 3
            },
            
            # Section 2: Basic Python Concepts
            {
                'course_id': course_id,
                'title': 'Basic Python Concepts',
                'type': 'text',
                'content': '<h3>Python Fundamentals</h3><p>In this section, we\'ll cover variables, data types, and basic operations.</p>',
                'order': 4,
                'is_section': True,
                'description': 'Learn about variables, data types, and basic operations',
                'quizzes': [
                    {
                        'title': 'Variables and Data Types Quiz',
                        'description': 'Test your understanding of Python variables and data types'
                    }
                ]
            },
            {
                'course_id': course_id,
                'title': 'Python Variables',
                'type': 'text',
                'content': '<p>Variables are containers for storing data values. Unlike other programming languages, Python has no command for declaring a variable. A variable is created the moment you first assign a value to it.</p><pre>x = 5\ny = "Hello, World!"</pre>',
                'order': 5
            },
            {
                'course_id': course_id,
                'title': 'Python Data Structure Visualization',
                'type': 'image',
                'content': 'https://pythontutor.com/visualize/img/python-list-visualization.png',
                'order': 6
            },
            
            # Section 3: Control Flow
            {
                'course_id': course_id,
                'title': 'Control Flow in Python',
                'type': 'text',
                'content': '<h3>Control Flow</h3><p>Learn how to control the flow of your Python programs using conditions and loops.</p>',
                'order': 7,
                'is_section': True,
                'description': 'Understanding conditions and loops in Python',
                'quizzes': [
                    {
                        'title': 'Control Flow Quiz',
                        'description': 'Test your understanding of if statements and loops'
                    }
                ]
            },
            {
                'course_id': course_id,
                'title': 'If Statements',
                'type': 'text',
                'content': '<p>Python supports the usual logical conditions from mathematics:</p><ul><li>Equals: a == b</li><li>Not Equals: a != b</li><li>Less than: a < b</li><li>Less than or equal to: a <= b</li><li>Greater than: a > b</li><li>Greater than or equal to: a >= b</li></ul>',
                'order': 8
            }
        ]
        
        # Insert all content items
        content_ids = mongo.db.course_content.insert_many(content_items).inserted_ids
        
        # Return success with course ID for testing
        return jsonify({
            'message': 'Test course created successfully',
            'course_id': str(course_id),
            'contentItemCount': len(content_ids)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/course/<course_id>/generate', methods=['POST'])
@jwt_required()
def generate_quiz(course_id):
    try:
        # Get the course to ensure it exists
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        # Get the request data
        data = request.get_json()
        if 'topic' not in data or 'num_questions' not in data:
            return jsonify({'error': 'Missing topic or num_questions'}), 400

        # Generate quiz questions using OpenAI
        prompt = f"Generate {data['num_questions']} multiple-choice quiz questions on the topic: {data['topic']}."
        response = AIclient.responses.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Parse the AI's response
        quiz_questions = response['choices'][0]['message']['content']
        print("Generated Questions:", quiz_questions)

        # Store the generated quiz in the database
        quiz = {
            "title": f"Quiz on {data['topic']}",
            "description": f"Automatically generated quiz on the topic: {data['topic']}",
            "course_id": ObjectId(course_id),
            "questions": quiz_questions,  # Store the raw AI response or parse it into structured data
            "created_at": datetime.utcnow()
        }
        mongo.db.quizzes.insert_one(quiz)

        return jsonify({"message": "Quiz generated and stored successfully", "quiz": quiz}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500