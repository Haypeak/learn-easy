from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def create_user(mongo, email, password):
    user = {
        "email": email,
        "password_hash": generate_password_hash(password).decode('utf-8'),
        "progress": []  # Track user progress
    }
    mongo.db.users.insert_one(user)

def check_user(mongo, email, password):
    user = mongo.db.users.find_one({"email": email})
    if user and check_password_hash(user["password_hash"], password):
        return create_access_token(identity=str(user["_id"]))
    return None
