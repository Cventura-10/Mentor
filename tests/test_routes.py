""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nimport pytest
from app import create_app, db
from config import TestConfig
from app.models import User
from flask import url_for
from flask_bcrypt import Bcrypt
from unittest.mock import patch

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

@pytest.fixture
def client():
    """Fixture to set up the test client and in-memory database."""
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def create_test_user():
    """Helper to create a test user with a Bcrypt hashed password."""
    hashed_password = bcrypt.generate_password_hash('Password123').decode('utf-8')
    user = User(username='testuser', email='test@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()

def test_register(client):
    """Test user registration with detailed debugging for redirects and content."""
    with client.application.app_context():
        # Attempt to register a new user
        response = client.post(url_for('main.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }, follow_redirects=True)

        # Print response data to debug
        print("\n--- Debugging registration response HTML ---")
        print(response.data.decode())

        # Check the status code for successful handling of registration
        assert response.status_code == 200, "Expected status code 200 for successful registration"

        # Look for specific success message or confirmation in the response
        assert (
            b"Your account has been created" in response.data or 
            b"Welcome" in response.data or 
            b"Login" in response.data  # Fall-back if redirect to login after registration
        ), "Registration confirmation message, welcome text, or redirect to login not found in response data."

        # Verify if the session or DB reflects the newly created user (optional)
        user = User.query.filter_by(username="newuser").first()
        assert user is not None, "New user was not created in the database."

def test_login(client):
    """Test login functionality."""
    with client.application.app_context():
        create_test_user()
        
        response = client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'Password123'
        }, follow_redirects=True)
        
        # Debugging print to understand HTML response if test fails
        print("\n--- Debugging login response HTML ---")
        print(response.data.decode())
        
        # Check for successful login and dashboard redirection
        assert response.status_code == 200
        assert b"Welcome back" in response.data or b"Dashboard" in response.data, \
            "Login message or dashboard text not found in response data."

@patch('app.main.routes.requests.post')
def test_create_meeting(mock_post, client):
    """Test meeting creation with a mocked Jitsi API response."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": "12345"}
    
    with client.application.app_context():
        create_test_user()
        
        # Log in the user to access the create meeting route
        client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'Password123'
        }, follow_redirects=True)
        
        # Test creating a meeting
        response = client.post(url_for('main.create_meeting'), follow_redirects=True)
        
        # Print the meeting creation HTML response for debugging
        print("\n--- Debugging meeting creation response HTML ---")
        print(response.data.decode())
        
        # Check if meeting creation was successful
        assert response.status_code == 200
        assert b"Meeting ID: 12345" in response.data or b"Meeting created successfully" in response.data, \
            "Meeting creation confirmation or meeting ID not found in response data."
