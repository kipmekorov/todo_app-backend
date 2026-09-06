from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)


#ЗАДАЧИ


class TaskShema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateShema(BaseModel):
    title: str


class TaskUpdateShema(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskShema] = []


@app.get("/tasks")
def read_tasks() -> list[TaskShema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateShema) -> TaskShema:
    new_task = TaskShema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateShema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed

            return task

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


#КАТЕГОРИИ


class CategoryShema(BaseModel):
    id: str
    name: str


class CategoryCreateShema(BaseModel):
    name: str


class CategoryUpdateShema(BaseModel):
    name: str


categories: list[CategoryShema] = []


@app.get("/categories")
def read_category() -> list[CategoryShema]:
    return categories

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateShema) -> CategoryShema:
    new_category = CategoryShema(id = str(uuid4()), name = payload.name)

    categories.append(new_category)
    return new_category


@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryUpdateShema):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name

            return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)