# main/routes.py
import os
import requests
from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)

JITSI_TOKEN = os.environ.get('JITSI_TOKEN', 'your_default_token')

# ... (rest of main routes) ...
