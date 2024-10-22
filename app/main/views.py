from flask import render_template
from app.models import Performance
from app.main import main

@main.route('/dashboard')
def dashboard():
    performances = Performance.query.all()

    # Calculate metrics
    avg_score = sum(p.score for p in performances) / len(performances) if performances else 0
    total_students = len(set(p.user_id for p in performances))
    
    return render_template('dashboard.html', avg_score=avg_score, total_students=total_students)
