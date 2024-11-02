# run.py

import os
from app import create_app, socketio  # Assuming 'create_app' and 'socketio' are in 'app' module

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Use socketio.run to start the app, ensuring compatibility with Flask-SocketIO
    port = int(os.getenv("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
