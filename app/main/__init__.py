import os
import requests
from functools import wraps
from flask import Blueprint, render_template, url_for, flash, redirect, request, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Achievement, UserProgress, MeetingHistory
from app.forms import LoginForm, RegistrationForm

# Define blueprint
main = Blueprint('main', __name__, template_folder='templates')

# Get Jitsi token from environment or use default
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
    return render_template('login.html', title='Login', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/create-meeting', methods=['POST'])
@login_required
def create_meeting():
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
        flash('Failed to create meeting. Try again later.', 'danger')
        print(f"Meeting creation error: {e}")
        return redirect(url_for('main.dashboard'))

@main.route('/meeting/<string:meeting_id>')
@login_required
def meeting(meeting_id):
    return render_template('meeting.html', title='Meeting', meeting_id=meeting_id)
