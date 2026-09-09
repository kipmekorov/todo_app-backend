from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key = True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategotyORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
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


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskShema:
    return TaskShema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskShema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateShema, db: Session = Depends(get_db)) -> TaskShema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    return task_orm_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateShema, db: Session = Depends(get_db)) -> TaskShema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    return task_orm_to_model(task_for_update)

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()


#КАТЕГОРИИ


class CategoryShema(BaseModel):
    id: str
    name: str


class CategoryCreateShema(BaseModel):
    name: str


class CategoryUpdateShema(BaseModel):
    name: str


def category_orm_model(category_orm: CategotyORM) -> CategoryShema:
    return CategoryShema(id=category_orm.id, name=category_orm.name)


@app.get("/categories")
def read_category(db: Session = Depends(get_db)) -> list[CategoryShema]:
    category_from_bd = db.scalars(select(CategotyORM)).all()
    return [category_orm_model(category) for category in category_from_bd]

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateShema, db: Session = Depends(get_db)) -> CategoryShema:
    new_category = CategotyORM(name = payload.name)
    db.add(new_category)
    db.commit()

    return category_orm_model(new_category)


@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryUpdateShema, db: Session = Depends(get_db)) -> CategoryShema:
    category_for_update = db.get(CategotyORM, category_id)
    if payload.name:
        category_for_update.name = payload.name
    db.commit()

    return category_orm_model(category_for_update)



@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    category_for_delete = db.get(CategotyORM, category_id)
    db.delete(category_for_delete)
    db.commit()
