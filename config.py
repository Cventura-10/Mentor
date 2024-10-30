import os
import secrets

class Config:
    # Generate a random secret key if not set in environment variables
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mentor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
