import os
import requests
from flask import (
    Blueprint, render_template, url_for, flash, redirect, 
    request, jsonify, session
)
from flask_login import (
    login_user, current_user, logout_user, login_required
)
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm

# Define the Blueprint
main = Blueprint('main', __name__)

# Jitsi token from environment variables (secure management)
JITSI_TOKEN = os.getenv('JITSI_TOKEN', 'Please_set_JITSI_TOKEN_in_env')

@main.route('/')
def home():
    print("Home route executed")
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
            next_page = request.args.get('next', 'main.dashboard')
            print(f"Redirecting to: {next_page}")
            return redirect(url_for(next_page))
        else:
            flash('Invalid email or password', 'danger')
            print("Login failed: Invalid credentials")

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

        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            print(f"Registration error: {e}")

    return render_template('register.html', title='Register', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    print(f"User {current_user.username} accessed the dashboard.")
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
    """Create a new Jitsi meeting and redirect to the meeting page."""
    api_url = "https://api.jitsi.me/createConference"
    headers = {
        "Authorization": f"Bearer {JITSI_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"name": "Mentor Meeting"}

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        meeting_id = response.json().get("id")

        if meeting_id:
            flash('Meeting created successfully!', 'success')
            return redirect(url_for('main.meeting', meeting_id=meeting_id))
        else:
            raise ValueError("Meeting ID not returned in response.")

    except (requests.RequestException, ValueError) as e:
        flash('Failed to create meeting. Try again later.', 'danger')
        print(f"Meeting creation error: {e}")
        return redirect(url_for('main.dashboard'))

@main.route('/meeting/<string:meeting_id>')
@login_required
def meeting(meeting_id):
    print(f"User {current_user.username} joined meeting {meeting_id}.")
    return render_template('meeting.html', title='Meeting', meeting_id=meeting_id)

@main.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    print(f"Accessed profile for user: {user.username}")
    return render_template('user_profile.html', title='User Profile', user=user)

@main.route('/api/register', methods=['POST'])
def api_register():
    form = RegistrationForm(request.json)
    if form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            print(f"API registration error: {e}")
            return jsonify({'error': 'Registration failed'}), 500

    return jsonify(form.errors), 400

@main.route('/api/login', methods=['POST'])
def api_login():
    form = LoginForm(request.json)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return jsonify({'message': 'User logged in successfully'}), 200
        else:
            print("API login failed: Invalid credentials")
            return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify(form.errors), 400

# Additional module routes
@main.route('/vr_experience')
def vr_experience():
    return render_template('vr_experience.html')

@main.route('/gamification')
def gamification():
    achievements = [
        {"title": "Quiz Master", "description": "Completed all quizzes with a high score!"},
        {"title": "Perfect Attendance", "description": "Attended all sessions in the last month."}
    ]
    progress = {"level": 5, "points": 1200}
    return render_template('gamificacion.html', achievements=achievements, progress=progress)

@main.route('/simulators')
def simulators():
    return render_template('simulators.html')

@main.route('/simulator_quiz')
def simulator_quiz():
    return render_template('simulator_quiz.html')

@main.route('/simulator_scenario')
def simulator_scenario():
    return render_template('simulator_scenario.html')
