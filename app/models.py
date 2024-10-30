from flask_login import UserMixin
from app import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'user'  # Explicit table name to avoid conflicts
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the password matches the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        """String representation of the User object."""
        return f"User('{self.username}', '{self.email}')"
