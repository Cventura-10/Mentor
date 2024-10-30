import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Heroku's port or default to 5000
    app.run(host="0.0.0.0", port=port)   # Bind to 0.0.0.0 for external visibility
