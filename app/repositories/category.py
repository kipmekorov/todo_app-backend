from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategotyORM


class CategoryRepository():
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategotyORM]:
        return self.db.scalars(select(CategotyORM))

    def get_by_id(self, category_id: int) -> CategotyORM:
        return self.db.get(CategotyORM, category_id)

    def create(self, name: str) -> CategotyORM:
        new_category = CategotyORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, CategotyORM) -> None:
        self.db.delete(CategotyORM)