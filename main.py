from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import asyncio


app = FastAPI()
tasks = {}


class Task(BaseModel):
    duration: int


@app.post("/task")
async def create_task(task: Task):
    task_id = str(uuid.uuid4())
    tasks[task_id] = asyncio.create_task(run_task(task.duration))
    return {"task_id": task_id}


async def run_task(duration: int):
    await asyncio.sleep(duration)


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.done():
        return {"status": "done"}
    else:
        return {"status": "running"}
