from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

@app.route('/')
def hello_world():
    """Returns a simple hello world message."""
    return 'Hello, world!'
