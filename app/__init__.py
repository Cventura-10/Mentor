import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from .celery_utils import make_celery  # Import make_celery from celery_utils

# Load environment variables from a .env file if available
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_object=None):
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists
    instance_path = os.path.join(app.instance_path)
    os.makedirs(instance_path, exist_ok=True)

    # Load configuration from provided object or environment variables
    if config_object:
        app.config.from_object(config_object)
    else:
        # Set rate limit storage URI with fallback to Redis
        app.config['RATELIMIT_STORAGE_URI'] = os.getenv('RATELIMIT_STORAGE_URI', 'redis://localhost:6379/0')
        # Load secret key and database URI from environment or defaults
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
        db_uri = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(instance_path, 'mentor.db')}")
        if db_uri.startswith("postgres://"):
            db_uri = db_uri.replace("postgres://", "postgresql://")
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'SimpleCache')
        app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    # Configure Flask-Login settings
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Create and configure Celery instance
    celery = make_celery(app)  # Create celery instance attached to this app

    # Define user_loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint, template_folder='templates')

    # Shell context for Flask CLI (for easy command line access)
    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Achievement, UserProgress, MeetingHistory
        return {
            'db': db,
            'app': app,
            'User': User,
            'Achievement': Achievement,
            'UserProgress': UserProgress,
            'MeetingHistory': MeetingHistory
        }

    # Add `current_year` to Jinja environment for templates
    app.jinja_env.globals['current_year'] = lambda: datetime.now().year

    return app
