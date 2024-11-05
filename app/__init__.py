import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Optional Celery Utils (if Celery is required)
try:
    from .celery_utils import make_celery
    CELERY_ENABLED = True
except ImportError:
    CELERY_ENABLED = False

# Load environment variables early
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
        db_uri = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'mentor.db')}")
        if db_uri.startswith("postgres://"):
            db_uri = db_uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'SimpleCache')
        app.config['RATELIMIT_STORAGE_URI'] = os.getenv('RATELIMIT_STORAGE_URI', 'redis://localhost:6379/0')
        app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    if CELERY_ENABLED:
        celery = make_celery(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, template_folder='templates')

    # Configure logging
    setup_logging(app)

    # Log each request for detailed access information
    @app.before_request
    def log_request_info():
        app.logger.info(f"Request: {request.method} {request.path}")

    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Achievement, UserProgress, MeetingHistory
        return {
            'db': db, 'app': app,
            'User': User, 'Achievement': Achievement,
            'UserProgress': UserProgress, 'MeetingHistory': MeetingHistory
        }

    app.jinja_env.globals['current_year'] = lambda: datetime.now().year

    return app

def setup_logging(app):
    """Set up logging for the application."""
    if not app.debug:
        file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)

        app.logger.info('Logging setup complete.')

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
