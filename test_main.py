import pytest
import asyncio
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/task", json={"duration": 5})
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data


@pytest.mark.asyncio
async def test_task_status():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post("/task", json={"duration": 1})
        task_id = create_response.json()["task_id"]
        status_response = await client.get(f"/task/{task_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["status"] == "running"
        await asyncio.sleep(1.5)
        final_status_response = await client.get(f"/task/{task_id}")
        assert final_status_response.status_code == 200
        final_status_data = final_status_response.json()
        assert final_status_data["status"] == "done"


@pytest.mark.asyncio
async def test_task_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/task/nonexistent_id")
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}
