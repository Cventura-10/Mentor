""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n# /Users/carlosventura/Mentor/educacion-singular-platform/simuladores_module/simuladores.py
from flask import render_template
from . import simuladores_bp

@simuladores_bp.route('/simulators')
def simulators():
    return render_template('simulators.html')
