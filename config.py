import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", 'mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority&appName=EAM-Cluster0')
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
