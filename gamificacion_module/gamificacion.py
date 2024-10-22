# /Users/carlosventura/Mentor/educacion-singular-platform/gamificacion_module/gamificacion.py
from flask import render_template
from . import gamificacion_bp

@gamificacion_bp.route('/gamification')
def gamification():
    return render_template('gamification.html')
