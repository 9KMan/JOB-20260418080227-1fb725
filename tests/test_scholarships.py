import pytest
from fastapi.testclient import TestClient


def test_create_scholarship(client):
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
        "/scholarships",
        json={
            "student_id": student_id,
            "items": [
                {"description": "Tuition", "amount": 500.00},
                {"description": "Books", "amount": 100.00}
            ],
            "total_amount": 600.00
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == "600.00"
    assert len(data["items"]) == 2


def test_list_scholarships(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    client.post("/scholarships", json={
        "student_id": student_id,
        "items": [{"description": "Tuition", "amount": 500.00}],
        "total_amount": 500.00
    })
    client.post("/scholarships", json={
        "student_id": student_id,
        "items": [{"description": "Full Package", "amount": 1000.00}],
        "total_amount": 1000.00
    })

    response = client.get("/scholarships")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_scholarship(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    create_response = client.post("/scholarships", json={
        "student_id": student_id,
        "items": [{"description": "Tuition", "amount": 500.00}],
        "total_amount": 500.00
    })
    scholarship_id = create_response.json()["id"]

    response = client.get(f"/scholarships/{scholarship_id}")
    assert response.status_code == 200
    assert float(response.json()["total_amount"]) == 500.00


def test_update_scholarship_status(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "first_name": "John",
        "last_name": "Doe"
    })
    student_id = student_response.json()["id"]

    create_response = client.post("/scholarships", json={
        "student_id": student_id,
        "items": [{"description": "Tuition", "amount": 500.00}],
        "total_amount": 500.00
    })
    scholarship_id = create_response.json()["id"]

    response = client.put(f"/scholarships/{scholarship_id}", json={"status": "partially_funded"})
    assert response.status_code == 200
    assert response.json()["status"] == "partially_funded"