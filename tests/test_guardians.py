import pytest
from fastapi.testclient import TestClient


def test_create_guardian(client):
    # Create school and student first
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    response = client.post(
        "/guardians",
        json={
            "student_id": student_id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@guardian.com",
            "phone": "+1234567890",
            "relationship_type": "mother"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["relationship_type"] == "mother"


def test_list_guardians(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    client.post("/guardians", json={"student_id": student_id, "first_name": "Guardian 1", "last_name": "Test"})
    client.post("/guardians", json={"student_id": student_id, "first_name": "Guardian 2", "last_name": "Test"})

    response = client.get("/guardians")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_guardian(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    create_response = client.post("/guardians", json={
        "student_id": student_id,
        "first_name": "Jane",
        "last_name": "Doe"
    })
    guardian_id = create_response.json()["id"]

    response = client.get(f"/guardians/{guardian_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"