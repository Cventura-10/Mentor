import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
from config import Config  # Import Config class

# Load .env variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directly set up Werkzeug logger to suppress specific static file logs
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Create app function
def create_app():
    app = Flask(__name__)
    
    # Use the Config class for setting configurations
    app.config.from_object(Config)

    # Fix Heroku Postgres connection string if necessary
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri.replace('postgres://', 'postgresql://')

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Adjust the login route as needed
    socketio.init_app(app)

    # Register blueprints
    from app.routes import main  # Import your blueprint here
    app.register_blueprint(main)  # Register the main blueprint

    # Suppress logging for static file requests in log_request_info
    @app.before_request
    def log_request_info():
        if request.path.startswith('/static/'):
            return  # Skip logging for static file requests

        # Log specific actions like login attempts
        if request.endpoint == 'main.login' and request.method == 'POST':
            if request.form.get('email'):
                logger.info(f"Login attempt for email: {request.form['email']}")

    # Example logging when accessing a restricted route
    @app.after_request
    def log_dashboard_access(response):
        if request.endpoint == 'main.dashboard':
            logger.info("Accessed Dashboard")
        return response

    return app

# The following code is usually included in `run.py` or equivalent
if __name__ == "__main__":
    app = create_app()
    socketio.run(app)  # Use socketio.run if socketio features are needed
