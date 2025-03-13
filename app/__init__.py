from flask import Flask, render_template_string
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

mongo = PyMongo()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    JWTManager(app)
    CORS(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.learning import learning_bp
    from app.routes.quiz import quiz_bp
    # from app.routes.tutor import tutor_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(learning_bp, url_prefix='/learning')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    
    @app.route('/')
    def index():
        return render_template_string("""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>API Status</title>
          </head>
          <body>
            <div class="container">
              <h1>API is working</h1>
              <p>Welcome to the API test page.</p>
            </div>
          </body>
        </html>
        """)

    # app.register_blueprint(tutor_bp, url_prefix='/tutor')

    return app
