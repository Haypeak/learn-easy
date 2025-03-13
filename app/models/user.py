from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def create_user(mongo, email, password, country_code=None, phone_number=None, first_name=None, last_name=None, level_of_education=None, school=None):
    user = {
        "email": email,
        "password_hash": generate_password_hash(password).decode('utf-8'),
        "country_code": country_code,
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "level_of_education": level_of_education,
        "school": school,
        "progress": []  # Track user progress
    }
    if mongo and mongo.db is not None:
        mongo.db.users.insert_one(user)
    else:
        raise ValueError("MongoDB connection is not initialized")

def check_user(mongo, email, password):
    user = mongo.db.users.find_one({"email": email})
    if user and check_password_hash(user["password_hash"], password):
        return create_access_token(identity=str(user["_id"]))
    return None
