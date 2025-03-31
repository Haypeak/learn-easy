from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/<quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id):
    try:
        quiz = mongo.db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404

        # Remove correct answers before sending to client
        questions = quiz.get('questions', [])
        for question in questions:
            if 'correct_answer' in question:
                del question['correct_answer']

        return jsonify({
            'id': str(quiz['_id']),
            'title': quiz['title'],
            'description': quiz.get('description', ''),
            'time_limit': quiz.get('time_limit', 0),
            'questions': questions,
            'total_points': quiz.get('total_points', 0)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/<quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'answers' not in data:
        return jsonify({'error': 'Missing answers'}), 400
        
    try:
        quiz = mongo.db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404

        # Calculate score
        total_points = 0
        max_points = 0
        results = []
        
        for question in quiz['questions']:
            max_points += question.get('points', 1)
            question_id = str(question['_id'])
            user_answer = next(
                (a['answer'] for a in data['answers'] 
                 if a['question_id'] == question_id), None)
            
            correct = False
            if user_answer is not None:
                correct = user_answer == question['correct_answer']
                if correct:
                    total_points += question.get('points', 1)
            
            results.append({
                'question_id': question_id,
                'correct': correct,
                'correct_answer': question['correct_answer'],
                'user_answer': user_answer
            })
        
        # Save quiz attempt
        attempt = {
            'user_id': ObjectId(current_user_id),
            'quiz_id': ObjectId(quiz_id),
            'score': total_points,
            'max_points': max_points,
            'results': results,
            'submitted_at': datetime.utcnow()
        }
        
        mongo.db.quiz_attempts.insert_one(attempt)
        
        return jsonify({
            'score': total_points,
            'max_points': max_points,
            'percentage': (total_points / max_points * 100) if max_points > 0 else 0,
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/course/<course_id>', methods=['GET'])
@jwt_required()
def get_course_quizzes(course_id):
    try:
        quizzes = list(mongo.db.quizzes.find({'course_id': ObjectId(course_id)}))
        return jsonify([{
            'id': str(quiz['_id']),
            'title': quiz['title'],
            'description': quiz.get('description', ''),
            'time_limit': quiz.get('time_limit', 0),
            'total_points': quiz.get('total_points', 0),
            'question_count': len(quiz.get('questions', []))
        } for quiz in quizzes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, jsonify
from app import mongo

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/quiz', methods=['GET'])
def get_quiz():
    quizzes = mongo.db.quizzes.find()
    return jsonify([{"id": str(q["_id"]), "question": q["question"], "options": q["options"]} for q in quizzes])
