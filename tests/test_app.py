"""Basic tests for the Flask application."""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test the landing page returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask SSH App" in response.data


def test_hello_page(client):
    """Test the greeting page returns HTML."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert b"Hello There!" in response.data


def test_api_status(client):
    """Test the JSON health-check endpoint."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["port"] == 5001


def test_404(client):
    """Test that a non-existent route returns 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
