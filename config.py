import os

class Config:
    MONGO_URI = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    OPENAI_API_KEY = "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"
