import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Set configurations from .env variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db_uri = os.getenv('DATABASE_URL')

    # Fixing Heroku postgres connection string if necessary
    if db_uri and db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///default.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    socketio.init_app(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
