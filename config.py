import os
import secrets

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mentor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis and Celery Configuration
    CACHE_TYPE = "RedisCache"  # Ensure Flask-Caching is set up with Redis
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Optional logging for better debugging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF in testing for easier form handling
    SERVER_NAME = "localhost.localdomain"  # Set server name for Flask testing
    LOG_LEVEL = 'DEBUG'
