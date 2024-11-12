from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import io
import base64

reporting = Blueprint('reporting', __name__)

@reporting.route('/report')
def report():
    # Generate a plot
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    plt.title("Sample Report")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render_template('report.html', plot_url=plot_url)
