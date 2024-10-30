import os  # Make sure to import os at the top
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

# Initialize extensions globally
db = SQLAlchemy()
bcrypt = Bcrypt()  # Ensure this is initialized globally
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)  # Now this will work correctly

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'mentor.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)  # This ensures bcrypt is initialized with the app
    login_manager.init_app(app)
    socketio.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Database creation if not exists
    db_path = os.path.join(app.instance_path, 'mentor.db')
    with app.app_context():
        if not os.path.exists(db_path):
            try:
                db.create_all()
                print(f"Database created at {db_path}.")
            except Exception as e:
                print(f"Error creating database: {e}")

    # Flask shell context for easier debugging
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app, 'User': User}

    return app
