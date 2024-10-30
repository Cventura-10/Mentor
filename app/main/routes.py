from app import db, bcrypt  # Import the global bcrypt instance directly
from flask import (
    Blueprint, render_template, url_for, flash, redirect, 
    request, session, jsonify
)
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm
import os
import requests

# Define the Blueprint
main = Blueprint('main', __name__)

# Jitsi token from environment variables
JITSI_TOKEN = os.getenv('JITSI_TOKEN', 'your_default_token')

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

        # Use bcrypt directly for password check
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next', 'main.dashboard')
            return redirect(url_for(next_page))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', title='Login', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Use bcrypt to hash the password
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
        # Use bcrypt to hash the password
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

        # Use bcrypt to check the password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
