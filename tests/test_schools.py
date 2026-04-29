import pytest
from fastapi.testclient import TestClient


def test_create_school(client):
    response = client.post(
        "/schools",
        json={"name": "Test School", "email": "test@school.com", "address": "123 Test St"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test School"
    assert data["email"] == "test@school.com"
    assert data["verification_status"] == "pending"


def test_list_schools(client):
    # Create a school first
    client.post("/schools", json={"name": "School 1", "email": "school1@test.com"})
    client.post("/schools", json={"name": "School 2", "email": "school2@test.com"})

    response = client.get("/schools")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_school(client):
    # Create a school
    create_response = client.post("/schools", json={"name": "Test School", "email": "test@school.com"})
    school_id = create_response.json()["id"]

    response = client.get(f"/schools/{school_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test School"


def test_get_school_not_found(client):
    response = client.get("/schools/99999")
    assert response.status_code == 404


def test_update_school(client):
    # Create a school
    create_response = client.post("/schools", json={"name": "Original Name", "email": "test@school.com"})
    school_id = create_response.json()["id"]

    response = client.put(f"/schools/{school_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_verify_school(client):
    # Create a school
    create_response = client.post("/schools", json={"name": "Test School", "email": "test@school.com"})
    school_id = create_response.json()["id"]

    response = client.post(f"/schools/{school_id}/verify")
    assert response.status_code == 200
    assert response.json()["verification_status"] == "verified"
    assert response.json()["verified_at"] is not None


def test_delete_school(client):
    # Create a school
    create_response = client.post("/schools", json={"name": "Test School", "email": "test@school.com"})
    school_id = create_response.json()["id"]

    response = client.delete(f"/schools/{school_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/schools/{school_id}")
    assert get_response.status_code == 404