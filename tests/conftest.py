# tests/conftest.py

import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()  # Setup in-memory database schema for each test
        yield app.test_client()  # Provide the test client for test cases
        db.drop_all()  # Cleanup schema after each test
