import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Run with dynamic port or default to 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
