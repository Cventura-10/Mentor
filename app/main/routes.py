""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nimport os
import requests
from flask import (
    Blueprint, render_template, url_for, flash, redirect, 
    request, session, jsonify, abort, current_app
)
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Achievement, UserProgress, MeetingHistory
from app.forms import LoginForm, RegistrationForm
from functools import wraps

main = Blueprint('main', __name__, template_folder='templates')
JITSI_TOKEN = os.getenv('JITSI_TOKEN', 'your_default_token')

# Role-based access control decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next') or url_for('main.dashboard')
            return redirect(next_page)
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'danger')
    return render_template('register.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/create-meeting', methods=['GET', 'POST'])
@login_required
def create_meeting():
    """Create a new Jitsi meeting and redirect to the meeting page."""
    if request.method == 'GET':
        # Render a form or informational page to create a meeting
        return render_template('create_meeting.html')

    try:
        api_url = "https://api.jitsi.me/createConference"
        headers = {
            "Authorization": f"Bearer {JITSI_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {"name": "Mentor Meeting"}
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        meeting_id = response.json().get("id")
        if meeting_id:
            new_meeting = MeetingHistory(user_id=current_user.id, meeting_id=meeting_id)
            db.session.add(new_meeting)
            db.session.commit()
            flash('Meeting created successfully!', 'success')
            return redirect(url_for('main.meeting', meeting_id=meeting_id))
        raise ValueError("Meeting ID not returned in response.")
    except (requests.RequestException, ValueError) as e:
        current_app.logger.error(f"Meeting creation error: {e}")
        flash('Failed to create meeting. Try again later.', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route('/meeting/<string:meeting_id>')
@login_required
def meeting(meeting_id):
    return render_template('meeting.html', meeting_id=meeting_id)

@main.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@main.route('/gamification')
@login_required
def gamification():
    achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    progress = UserProgress.query.filter_by(user_id=current_user.id).first()
    return render_template('gamification.html', achievements=achievements, progress=progress)

@main.route('/virtual_classrooms')
@login_required
def virtual_classrooms():
    return render_template('virtual_classrooms.html')

@main.route('/vr_experience')
def vr_experience():
    return render_template('vr_experience.html')

@main.route('/simulators')
def simulators():
    return render_template('simulators.html')

@main.route('/simulator_quiz')
def simulator_quiz():
    return render_template('simulator_quiz.html')

@main.route('/simulator_scenario')
def simulator_scenario():
    return render_template('simulator_scenario.html')

@main.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@main.route('/report')
@login_required
def report():
    return render_template('report.html')

# Error handler
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
