""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n# simuladores_module/routes.py
from flask import render_template
from . import simuladores_bp

@simuladores_bp.route('/simulators')
def simulators_home():
    return render_template('simulators/home.html')

@simuladores_bp.route('/simulators/quiz')
def simulators_quiz():
    return render_template('simulators/quiz.html')

@simuladores_bp.route('/simulators/scenario')
def simulators_scenario():
    return render_template('simulators/scenario.html')
