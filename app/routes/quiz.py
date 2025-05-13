from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId
from datetime import datetime
import openai

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/<quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id):
    try:
        quiz = mongo.db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404

        # Get section information if available
        section_info = None
        if 'section_id' in quiz and 'course_id' in quiz:
            course = mongo.db.courses.find_one(
                {'_id': quiz['course_id']},
                {'structure.sections': 1}
            )
            if course and 'structure' in course and 'sections' in course['structure']:
                for section in course['structure']['sections']:
                    if str(section.get('_id')) == str(quiz['section_id']):
                        section_info = section
                        break

        # Remove correct answers before sending to client
        questions = quiz.get('questions', [])
        for question in questions:
            if 'correct_answer' in question:
                del question['correct_answer']

        response_data = {
            'id': str(quiz['_id']),
            'title': quiz['title'],
            'description': quiz.get('description', ''),
            'time_limit': quiz.get('time_limit', 0),
            'questions': questions,
            'total_points': quiz.get('total_points', 0)
        }

        # Add section information if available
        if 'section_id' in quiz:
            response_data['section_id'] = str(quiz['section_id'])
        
        if section_info:
            response_data['section_title'] = section_info.get('title', 'Unknown Section')

        # Add course information if available
        if 'course_id' in quiz:
            response_data['course_id'] = str(quiz['course_id'])

        return jsonify(response_data), 200
    except Exception as e:
        print(f"Error in get_quiz: {str(e)}")
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
            'course_id': quiz.get('course_id'),  # Store course ID if available
            'section_id': quiz.get('section_id'),  # Store section ID if available
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
        print(f"Error in submit_quiz: {str(e)}")
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/course/<course_id>/generate', methods=['POST'])
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

        topic = data['topic']
        num_questions = data['num_questions']

        # # Use OpenAI to generate quiz questions
        # openai.api_key = "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"  # Replace with your OpenAI API key
        # prompt = (
        #     f"Generate {num_questions} multiple-choice questions on the topic '{topic}'. "
        #     "Each question should include 4 options and indicate the correct answer."
        # )
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=1500,
        #     n=1,
        #     stop=None,
        #     temperature=0.7
        # )

        # # Parse the AI response
        # questions = []
        # ai_output = response.choices[0].text.strip().split("\n\n")
        # for q in ai_output:
        #     lines = q.split("\n")
        #     if len(lines) < 5:
        #         continue
        #     question_text = lines[0]
        #     options = lines[1:5]
        #     correct_answer = lines[5].split(":")[-1].strip() if len(lines) > 5 else None
        #     questions.append({
        #         'text': question_text,
        #         'options': [opt.split(" ", 1)[-1] for opt in options],
        #         'correct_answer': correct_answer,
        #         'points': 1
        #     })

        # # Create the quiz document
        # quiz = {
        #     'course_id': ObjectId(course_id),
        #     'title': f"Quiz on {topic}",
        #     'description': f"A quiz generated on the topic '{topic}'",
        #     'time_limit': data.get('time_limit', 0),
        #     'total_points': len(questions),
        #     'questions': questions,
        #     'created_at': datetime.utcnow()
        # }

        # # Insert the quiz into the database
        # result = mongo.db.quizzes.insert_one(quiz)

        # return jsonify({'message': 'Quiz generated successfully', 'quiz_id': str(result.inserted_id)}), 201
        return jsonify({'message': 'Not yet Implemented'}), 201
    except Exception as e:
        print(f"Error in generate_quiz: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@quiz_bp.route('/course/<course_id>', methods=['GET'])
@jwt_required()
def get_course_quizzes(course_id):
    try:
        # First, get the course to retrieve its structure
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        # Create a map of section IDs to their details for easier lookup
        section_map = {}
        if 'structure' in course and 'sections' in course['structure']:
            for section in course['structure']['sections']:
                if 'id' in section:
                    section_map[str(section['id'])] = section
        
        # Get all quizzes for this course
        quizzes = list(mongo.db.quizzes.find({'course_id': ObjectId(course_id)}))
        
        # Format quiz data with section information
        formatted_quizzes = []
        for quiz in quizzes:
            quiz_data = {
                'id': str(quiz['id']),
                'title': quiz['title'],
                'description': quiz.get('description', ''),
                'time_limit': quiz.get('time_limit', 0),
                'total_points': quiz.get('total_points', 0),
                'question_count': len(quiz.get('questions', []))
            }
            
            # Add section information if available
            if 'section_id' in quiz:
                section_id = str(quiz['section_id'])
                quiz_data['section_id'] = section_id
                
                # Include section title if the section exists in the course structure
                if section_id in section_map:
                    quiz_data['section_title'] = section_map[section_id].get('title', 'Unknown Section')
            
            formatted_quizzes.append(quiz_data)
        
        return jsonify(formatted_quizzes), 200
    except Exception as e:
        print(f"Error in get_course_quizzes: {str(e)}")
        return jsonify({'error': str(e)}), 500
