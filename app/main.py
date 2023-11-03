"""Entry point of the server"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    """Health check function"""
    return "Hello, World!"
