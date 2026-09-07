"""Basic tests for the Flask application."""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the health-check / landing endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "message" in data


def test_hello(client):
    """Test the greeting endpoint."""
    response = client.get("/hello")
    assert response.status_code == 200
    data = response.get_json()
    assert "greeting" in data
    assert "Hello" in data["greeting"]


def test_404(client):
    """Test that a non-existent route returns 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
