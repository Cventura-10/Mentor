"""
Module Purpose: This module initializes and configures the Flask application, including loading environment variables, 
setting up extensions, and registering blueprints.
Dependencies: Flask, SQLAlchemy, Flask-Bcrypt, Flask-Login, Flask-Migrate, Flask-SocketIO, Flask-Caching, Flask-Limiter, python-dotenv
"""

import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Initialize extensions without app context
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

# Use gevent as the async_mode for SocketIO
socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")

def create_app(config_class=None):
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Load configuration from the environment or fallback to default
    config_class = config_class or os.getenv('FLASK_CONFIG', 'config.Config')
    app.config.from_object(config_class)

    # Initialize extensions with app context
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        socketio.init_app(app)  # SocketIO initialized with gevent
        cache.init_app(app)
        limiter.init_app(app)
    except Exception as e:
        print(f"Error initializing extensions: {e}")

    # Configure LoginManager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Register a global Jinja function for the current year
    app.jinja_env.globals['current_year'] = lambda: datetime.now().year

    # Import and register the main blueprint (moved inside to avoid circular imports)
    from app.main.routes import main  # Ensure 'main' is defined in 'app/main/routes.py'
    app.register_blueprint(main)

    return app
