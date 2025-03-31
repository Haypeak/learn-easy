from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def create_user(mongo, email, password, country_code=None, phone_number=None, full_name=None, level_of_education=None, school=None, learning_goal=None, formYear=None):
    user = {
        "email": email,
        "password_hash": generate_password_hash(password).decode('utf-8'),
        "country_code": country_code,
        "phone_number": phone_number,
        "full_name": full_name,
        "level_of_education": level_of_education,
        "school": school,
        "learning_goal": learning_goal,
        "progress": [],  # Track user progress
        "subjects": [],
        "formYear": formYear
    }
    if mongo and mongo.db is not None:
        mongo.db.users.insert_one(user)
    else:
        raise ValueError("MongoDB connection is not initialized")
    return mongo.db.users.find_one({"email":user["email"]})


def update_user(mongo, user_id, formYear=None, subjects=None, progress=None, phone_number=None, country_code=None, school=None, learning_goals=None, education_level=None):
    update_data = {}
    
    if education_level is not None:
        update_data["level_of_education"] = education_level
    if school is not None:
        update_data["school"] = school
    if learning_goals is not None:
        update_data["learning_goals"] = learning_goals
    if phone_number is not None:
        update_data["phone_number"]
    if country_code is not None:
        update_data["country_code"]
    if formYear is not None:
        update_data['formYear']
    if subjects is not None:
        update_data[subjects]
    if progress is not None:
        update_data[progress]

    if not update_data:
        raise ValueError("No valid fields provided to update")

    if mongo and mongo.db is not None:
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    else:
        raise ValueError("MongoDB connection is not initialized")

def check_user(mongo, email, password):
    user = mongo.db.users.find_one({"email": email})
    if user and check_password_hash(user["password_hash"], password):
        return create_access_token(identity=str(user["_id"]))
    return None
