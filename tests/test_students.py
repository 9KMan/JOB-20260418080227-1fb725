import pytest
from fastapi.testclient import TestClient


def test_create_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    response = client.post(
        "/students",
        json={
            "school_id": school_id,
            "name": "John Doe",
            "email": "john@student.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["school_id"] == school_id


def test_list_students(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    client.post("/students", json={"school_id": school_id, "name": "Student 1 Test"})
    client.post("/students", json={"school_id": school_id, "name": "Student 2 Test"})

    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "name": "John Doe"})
    student_id = create_response.json()["id"]

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"


def test_update_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "name": "John Doe"})
    student_id = create_response.json()["id"]

    response = client.put(f"/students/{student_id}", json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


def test_delete_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "name": "John Doe"})
    student_id = create_response.json()["id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204