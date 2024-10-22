from flask import Blueprint

reporting = Blueprint('reporting', __name__)

from . import views  # Ensure this import exists to register the views
