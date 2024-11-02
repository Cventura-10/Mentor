from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def is_admin(self):
        return self.role == 'admin'

class MeetingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    meeting_id = db.Column(db.String(60), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='meeting_histories', lazy=True)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user = db.relationship('User', backref='achievements', lazy=True)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    level = db.Column(db.Integer, default=1)
    points = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref='progress', lazy=True)

    def update_level(self):
        self.level = self.points // 100
        db.session.commit()
