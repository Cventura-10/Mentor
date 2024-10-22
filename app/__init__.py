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
    db_uri = os.getenv('DATABASE_URL') or 'sqlite:///mentor.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Initialize app with extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    socketio.init_app(app)

    # Import models and set up user loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Register reporting blueprint
    from app.reporting import reporting
    app.register_blueprint(reporting, url_prefix='/reporting')

    return app
