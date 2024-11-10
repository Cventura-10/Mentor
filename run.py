"""
Module Purpose: This module serves as the entry point for running the application.
Dependencies: 
- os: For environment variable handling.
- app: Includes the create_app function and socketio for socket communication.
"""

import os
from app import create_app, socketio  # Ensure this imports the correct create_app function

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Define the port number from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Start the application with socketio, accessible externally
    socketio.run(app, host="0.0.0.0", port=port)
