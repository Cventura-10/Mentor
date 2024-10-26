import os
import requests
from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm

# Initialize the Blueprint
main = Blueprint('main', __name__)

# Environment variable for Jitsi token
JITSI_TOKEN = os.environ.get('JITSI_TOKEN', 'your_default_token')

# Home route
@main.route('/')
def home():
    print("Home route executed")
    return render_template('index.html')  # Ensure this template exists

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register', form=form)

# Dashboard route
@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

# Logout route
@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Create meeting route
@main.route('/create-meeting', methods=['GET', 'POST'])
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
        meeting_id = response.json()["id"]
        return redirect(url_for('main.meeting', meeting_id=meeting_id))
    except requests.RequestException:
        flash('Failed to create meeting', 'danger')
        return redirect(url_for('main.dashboard'))

# Meeting route
@main.route('/meeting/<string:meeting_id>', methods=['GET'])
@login_required
def meeting(meeting_id):
    return render_template('meeting.html', title='Meeting', meeting_id=meeting_id)

# User profile route
@main.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', title='User Profile', user=user)

# API route for registration
@main.route('/api/register', methods=['POST'])
def api_register():
    form = RegistrationForm(request.json)
    if form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered'}), 201
    return jsonify(form.errors), 400

# API route for login
@main.route('/api/login', methods=['POST'])
def api_login():
    form = LoginForm(request.json)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return jsonify({'message': 'User logged in'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
