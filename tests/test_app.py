import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: Get activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test: Signup for activity
def test_signup_for_activity():
    activity = "Chess Club"
    email = "testuser@example.com"
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Second signup should fail (duplicate)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

# Test: Unregister from activity
def test_unregister_from_activity():
    activity = "Chess Club"
    email = "testuser@example.com"
    # Unregister should succeed
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()
