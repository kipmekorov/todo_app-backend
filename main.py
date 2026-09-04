from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


class TaskShema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateShema(BaseModel):
    title: str


tasks: list[TaskShema] = []


@app.get("/tasks")
def read_tasks() -> list[TaskShema]:
    return tasks


@app.post("/tasks")
def create_task(payload: TaskCreateShema) -> TaskShema:
    new_task = TaskShema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task