import pytest
from fastapi.testclient import TestClient


def test_create_student(client):
    # First create a school
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    response = client.post(
        "/students",
        json={
            "school_id": school_id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@student.com",
            "phone": "+1234567890"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["school_id"] == school_id


def test_list_students(client):
    # Create school and students
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    client.post("/students", json={"school_id": school_id, "first_name": "Student 1", "last_name": "Test"})
    client.post("/students", json={"school_id": school_id, "first_name": "Student 2", "last_name": "Test"})

    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "first_name": "John", "last_name": "Doe"})
    student_id = create_response.json()["id"]

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


def test_update_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "first_name": "John", "last_name": "Doe"})
    student_id = create_response.json()["id"]

    response = client.put(f"/students/{student_id}", json={"first_name": "Jane"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"


def test_delete_student(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    create_response = client.post("/students", json={"school_id": school_id, "first_name": "John", "last_name": "Doe"})
    student_id = create_response.json()["id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204