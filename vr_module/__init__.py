# /Users/carlosventura/Mentor/educacion-singular-platform/vr_module/__init__.py
from flask import Blueprint

vr_bp = Blueprint('vr', __name__, template_folder='templates')

from . import vr
