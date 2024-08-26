import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/task", json={"duration": 5})
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data

def test_task_status():
    create_response = client.post("/task", json={"duration": 1})
    task_id = create_response.json()["task_id"]


    status_response = client.get(f"/task/{task_id}")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["status"] == "running"


    import time
    time.sleep(1.5)


    final_status_response = client.get(f"/task/{task_id}")
    assert final_status_response.status_code == 200
    final_status_data = final_status_response.json()
    assert final_status_data["status"] == "done"

def test_task_not_found():
    response = client.get("/task/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
