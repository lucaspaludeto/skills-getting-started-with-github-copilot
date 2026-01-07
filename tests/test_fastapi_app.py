import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball Team" in data
    assert "Soccer Club" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Art Club"
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity():
    email = "unregisterstudent@mergington.edu"
    activity = "Drama Club"
    # Sign up first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"
