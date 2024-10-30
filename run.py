from gevent import monkey
monkey.patch_all()  # Ensure this is at the top for gevent compatibility

import os
from app import create_app, socketio

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Get the port from the Heroku environment, default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    # Run the app on the assigned port, using gevent-based socketio
    socketio.run(app, host="0.0.0.0", port=port)
