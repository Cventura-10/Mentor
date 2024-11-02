import os
import secrets

class Config:
    # Use a secure, randomly generated key if not provided in the environment
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mentor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis and Celery configuration for caching and background tasks
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier testing
    SERVER_NAME = "localhost.localdomain"  # Necessary for tests that require a server name
