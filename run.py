# run.py

from app import create_app, socketio  # Assuming 'create_app' and 'socketio' are in 'app' module

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Use socketio.run to start the app, ensuring compatibility with Flask-SocketIO
    socketio.run(app)
