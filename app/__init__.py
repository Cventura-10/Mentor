# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()

def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure the instance folder exists for SQLite DB file
    os.makedirs(app.instance_path, exist_ok=True)

    # Configure the database, defaulting to SQLite if DATABASE_URL is not set
    uri = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'mentor.db')}")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)  # Ensures compatibility with PostgreSQL on Heroku

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login configuration
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.main.routes import main
    app.register_blueprint(main)

    from app.users.routes import users
    app.register_blueprint(users, url_prefix='/users')

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Shell context for flask shell
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'app': app}

    return app
