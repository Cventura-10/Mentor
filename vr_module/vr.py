# /Users/carlosventura/Mentor/educacion-singular-platform/vr_module/vr.py
from flask import render_template
from . import vr_bp

@vr_bp.route('/vr')
def vr():
    return render_template('vr.html')
