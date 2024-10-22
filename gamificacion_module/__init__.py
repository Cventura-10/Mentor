# /Users/carlosventura/Mentor/educacion-singular-platform/gamificacion_module/__init__.py
from flask import Blueprint

gamificacion_bp = Blueprint('gamificacion', __name__, template_folder='templates')

from . import gamificacion
