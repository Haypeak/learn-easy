from flask import Blueprint, request, jsonify
from app.services.ai_tutor import ask_ai

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/ask-tutor', methods=['POST'])
def ask_tutor():
    data = request.get_json()
    response = ask_ai(data["question"])
    return jsonify({"response": response})




