from flask import Blueprint, jsonify
from app import mongo

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/quiz', methods=['GET'])
def get_quiz():
    quizzes = mongo.db.quizzes.find()
    return jsonify([{"id": str(q["_id"]), "question": q["question"], "options": q["options"]} for q in quizzes])
