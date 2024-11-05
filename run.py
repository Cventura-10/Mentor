import os
from app import create_app, socketio  # Make sure this imports the correct `create_app` function

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)  # Use host "0.0.0.0" to accept external connections
