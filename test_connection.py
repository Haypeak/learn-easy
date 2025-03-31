# from flask import Flask, jsonify
# from flask_pymongo import PyMongo

# # Flask app setup
# app = Flask(__name__)

# # MongoDB URI
# app.config["MONGO_URI"] = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"

# # Initialize PyMongo
# mongo = PyMongo(app)

# # Test MongoDB connection route
# @app.route('/test-mongo', methods=['GET'])
# def test_mongo():
#     try:
#         # Insert a test document
#         test_collection = mongo.db.test_collection
#         test_document = {"name": "Test User", "email": "test@example.com"}
#         test_collection.insert_one(test_document)

#         # Retrieve the inserted document
#         retrieved_document = test_collection.find_one({"email": "test@example.com"})
#         return jsonify({
#             "message": "MongoDB connection successful!",
#             "retrieved_document": {
#                 "name": retrieved_document["name"],
#                 "email": retrieved_document["email"]
#             }
#         }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from werkzeug.security import generate_password_hash
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority")
db = client["Learn_Easy"]

# Update password hashes for all users
users = db.users.find()
for user in users:
    if "password_hash" not in user or not user["password_hash"]:
        new_password_hash = generate_password_hash("defaultpassword123")  # Replace with actual password logic
        db.users.update_one({"_id": user["_id"]}, {"$set": {"password_hash": new_password_hash}})