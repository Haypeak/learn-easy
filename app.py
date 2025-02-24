# app.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/'
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")

mongo = PyMongo(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
from routes.questions import questions_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(questions_bp, url_prefix='/api/questions')

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)))
