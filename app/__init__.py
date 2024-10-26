import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

# Initialize extensions (without app context)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')

    # Fix Heroku postgres connection string if needed
    db_uri = os.getenv('DATABASE_URL')
    if db_uri and db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://')
    else:
        db_uri = 'sqlite:///mentor.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app context
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # User loader function for Flask-Login
    from app.models import User  # Import models here, after db is initialized

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
