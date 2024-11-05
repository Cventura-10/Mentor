import os
import requests
import logging
from functools import wraps
from flask import (
    Blueprint, render_template, url_for, flash, redirect, 
    request, session, abort, current_app, jsonify
)
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Achievement, UserProgress, MeetingHistory
from app.forms import LoginForm, RegistrationForm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define blueprint
main = Blueprint('main', __name__, template_folder='templates')

# Jitsi token for meeting creation
JITSI_TOKEN = os.getenv('JITSI_TOKEN', 'your_default_token')

# Admin role check decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
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
    return render_template('login.html', title='Login', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
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
    return render_template('register.html', title='Register', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route."""
    return render_template('dashboard.html', title='Dashboard')

@main.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/create-meeting', methods=['GET', 'POST'])
@login_required
def create_meeting():
    """Create a new Jitsi meeting and redirect to the meeting page."""
    if request.method == 'GET':
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
        if not meeting_id:
            raise ValueError("Meeting ID not returned in response.")
        
        new_meeting = MeetingHistory(user_id=current_user.id, meeting_id=meeting_id)
        db.session.add(new_meeting)
        db.session.commit()
        flash('Meeting created successfully!', 'success')
        return redirect(url_for('main.meeting', meeting_id=meeting_id))
    
    except (requests.RequestException, ValueError) as e:
        current_app.logger.error(f"Meeting creation error: {e}")
        flash('Failed to create meeting. Try again later.', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route('/meeting/<string:meeting_id>')
@login_required
def meeting(meeting_id):
    """Display meeting details."""
    return render_template('meeting.html', title='Meeting', meeting_id=meeting_id)

@main.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    """User profile page."""
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@main.route('/gamification')
@login_required
def gamification():
    """Gamification route."""
    achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    progress = UserProgress.query.filter_by(user_id=current_user.id).first()
    return render_template('gamification.html', achievements=achievements, progress=progress)

@main.route('/virtual_classrooms')
@login_required
def virtual_classrooms():
    """Virtual classrooms page."""
    return render_template('virtual_classrooms.html')

@main.route('/vr_experience')
def vr_experience():
    """Virtual Reality Experience page."""
    return render_template('vr_experience.html')

@main.route('/simulators')
def simulators():
    """Simulators overview page."""
    return render_template('simulators.html')

@main.route('/simulator_quiz')
def simulator_quiz():
    """Simulators quiz page."""
    return render_template('simulator_quiz.html')

@main.route('/simulator_scenario')
def simulator_scenario():
    """Simulators scenario page."""
    return render_template('simulator_scenario.html')

@main.route('/notifications')
@login_required
def notifications():
    """Notifications page."""
    return render_template('notifications.html')

@main.route('/report')
@login_required
def report():
    """Report page."""
    return render_template('report.html')

# Error handler for 404
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
