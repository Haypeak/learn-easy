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
