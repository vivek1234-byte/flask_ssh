"""Sample Flask application for the Jenkins CI/CD pipeline."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Health-check / landing endpoint."""
    return jsonify(status="ok", message="Flask app is running!")


@app.route("/hello")
def hello():
    """Simple greeting endpoint."""
    return jsonify(greeting="Hello from the Jenkins-built Flask app!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
