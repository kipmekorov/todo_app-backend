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


class BookShema(BaseModel):
    book: str


tasks: list[TaskShema] = []


@app.get("/tasks")
def read_tasks() -> list[TaskShema]:
    return tasks


@app.post("/tasks")
def create_task(payload: TaskCreateShema) -> TaskShema:
    new_task = TaskShema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task


book = ""


@app.get("/book")
def get_book():
    if book:
        return {"message": f"Любимая книга: {book}"}
    return {"message": "Книга не задана"}


@app.post("/book")
def set_book(payload: BookShema):
    global book
    book = payload.book
    return {"message": f"Книга '{book}' сохранена"}