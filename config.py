import os

class Config:
    MONGO_URI = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    # OPEN_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
