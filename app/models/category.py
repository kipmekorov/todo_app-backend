from sqlalchemy.orm import Mapped

from .base import Base


class CategotyORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]
