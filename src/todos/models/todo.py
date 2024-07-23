from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.databases.models.db_context import DBContext
from src.todos.enums.todo import TodoStatus


class Todo(DBContext):
    __tablename__ = "todos"

    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus), default=TodoStatus.PENDING, nullable=False
    )
