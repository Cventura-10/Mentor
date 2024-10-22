from flask import Blueprint, render_template
import matplotlib.pyplot as plt

reporting = Blueprint('reporting', __name__)

@reporting.route('/report')
def report():
    # Example plot creation
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    plt.title("Sample Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.savefig('static/plot.png')
    plt.clf()
    
    return render_template('report.html', image_file='plot.png')
