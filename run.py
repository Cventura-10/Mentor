# run.py
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(port=5001)  # Specify a different port here
