from flask import Blueprint

# Define the Blueprint
main = Blueprint('main', __name__)

# Import routes to avoid circular imports
from app.main import routes
