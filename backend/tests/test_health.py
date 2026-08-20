"""Health check endpoint pytest unit test."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Uniplexity Migration Agent"
    assert data["status"] == "running"

def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
