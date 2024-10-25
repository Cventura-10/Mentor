import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')

    # Fix for Heroku's postgres connection string if needed
    db_uri = os.getenv('DATABASE_URL')
    if db_uri and db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://')
    else:
        db_uri = 'sqlite:///mentor.db'  # Local SQLite fallback

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'users.login'

    # Import models to use with login_manager
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.users.routes import users
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
