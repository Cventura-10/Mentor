# app/main/__init__.py
from flask import Blueprint

# Define the Blueprint
main = Blueprint('main', __name__)

# Import routes to register them with the blueprint
# This is placed after defining `main` to avoid circular imports
from app.main import routes
