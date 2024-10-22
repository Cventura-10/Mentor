# /Users/carlosventura/Mentor/educacion-singular-platform/simuladores_module/simuladores.py
from flask import render_template
from . import simuladores_bp

@simuladores_bp.route('/simulators')
def simulators():
    return render_template('simulators.html')
