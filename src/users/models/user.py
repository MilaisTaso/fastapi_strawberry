from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.databases.models.db_context import DBContextWithDeletedAt


class User(DBContextWithDeletedAt):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    nick_name: Mapped[str] = mapped_column(String(40))

    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
