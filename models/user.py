# models/user.py
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = PyMongo()

class User:
    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({"username": username, "password": hashed_password})

    @staticmethod
    def find_user(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password'], password)
