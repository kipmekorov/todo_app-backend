from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key = True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Коллекция не найдена")


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Коллекция не найдена")
