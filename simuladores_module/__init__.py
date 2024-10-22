# simuladores_module/__init__.py
from flask import Blueprint

simuladores_bp = Blueprint('simuladores', __name__)

from . import routes
