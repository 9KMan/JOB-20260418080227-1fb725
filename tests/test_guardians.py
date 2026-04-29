import pytest
from fastapi.testclient import TestClient


def test_create_guardian(client):
    response = client.post(
        "/guardians",
        json={
            "name": "Jane Doe",
            "email": "jane@guardian.com",
            "phone": "+1234567890",
            "relationship_type": "mother"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["relationship_type"] == "mother"


def test_list_guardians(client):
    client.post("/guardians", json={"name": "Guardian 1", "email": "g1@test.com"})
    client.post("/guardians", json={"name": "Guardian 2", "email": "g2@test.com"})

    response = client.get("/guardians")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_guardian(client):
    create_response = client.post("/guardians", json={
        "name": "Jane Doe",
        "email": "jane@guardian.com"
    })
    guardian_id = create_response.json()["id"]

    response = client.get(f"/guardians/{guardian_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"
