from app import app, events, Event
import pytest

@pytest.fixture(autouse=True)
def reset_data():
    # Reset the in-memory "database" before each test
    events.clear()
    events.append(Event(1, "Tech Meetup"))
    events.append(Event(2, "Python Workshop"))

def test_create_event():
    client = app.test_client()
    response = client.post("/events", json={"title": "Hackathon"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data and data["title"] == "Hackathon"


def test_create_event_uses_unique_id_after_delete():
    client = app.test_client()
    client.delete("/events/1")

    response = client.post("/events", json={"title": "Hackathon"})

    assert response.status_code == 201
    assert response.get_json() == {"id": 3, "title": "Hackathon"}


def test_create_event_requires_non_empty_title():
    client = app.test_client()

    response = client.post("/events", json={"title": "  "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Title is required"}


def test_create_event_rejects_invalid_json():
    client = app.test_client()

    response = client.post("/events", data="{", content_type="application/json")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid JSON payload"}


def test_update_event():
    client = app.test_client()
    response = client.patch("/events/1", json={"title": "Hackathon 2025"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Hackathon 2025"

def test_update_event_not_found():
    client = app.test_client()
    response = client.patch("/events/99", json={"title": "Ghost Event"})
    assert response.status_code == 404

def test_delete_event():
    client = app.test_client()
    response = client.delete("/events/2")
    assert response.status_code == 204

def test_delete_event_not_found():
    client = app.test_client()
    response = client.delete("/events/99")
    assert response.status_code == 404
