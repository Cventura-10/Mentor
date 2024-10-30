import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate

# Initialize extensions globally
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()

def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

    # Handle DATABASE_URL for PostgreSQL compatibility
    uri = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'mentor.db')}")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login configuration
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.users.routes import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Flask shell context for easier debugging
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app, 'User': User}

    return app
