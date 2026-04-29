import pytest
from fastapi.testclient import TestClient


def test_create_agent(client):
    response = client.post(
        "/agents",
        json={
            "name": "Test Agent",
            "email": "agent@test.com",
            "phone": "+1234567890"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Agent"
    assert data["is_active"] is True


def test_list_agents(client):
    client.post("/agents", json={"name": "Agent 1", "email": "agent1@test.com"})
    client.post("/agents", json={"name": "Agent 2", "email": "agent2@test.com"})

    response = client.get("/agents")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_agent(client):
    create_response = client.post("/agents", json={"name": "Test Agent", "email": "agent@test.com"})
    agent_id = create_response.json()["id"]

    response = client.get(f"/agents/{agent_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Agent"


def test_update_agent(client):
    create_response = client.post("/agents", json={"name": "Original Name", "email": "agent@test.com"})
    agent_id = create_response.json()["id"]

    response = client.put(f"/agents/{agent_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_assign_student_to_agent(client):
    school_response = client.post("/schools", json={"name": "Test School", "email": "school@test.com"})
    school_id = school_response.json()["id"]

    student_response = client.post("/students", json={
        "school_id": school_id,
        "name": "John Doe"
    })
    student_id = student_response.json()["id"]

    agent_response = client.post("/agents", json={"name": "Test Agent", "email": "agent@test.com"})
    agent_id = agent_response.json()["id"]

    response = client.post(f"/agents/{agent_id}/students/{student_id}")
    assert response.status_code == 201