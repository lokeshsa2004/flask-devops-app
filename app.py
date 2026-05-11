# -*- coding: utf-8 -*-

from app import create_app

# Create Flask app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
