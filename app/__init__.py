from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
