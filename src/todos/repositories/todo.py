from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.bases import DatabaseRepository
from src.todos.models.todo import Todo
from src.todos.schemas.todo import CreateTodo, UpdateTodo


class TodoRepository(DatabaseRepository[Todo, CreateTodo, UpdateTodo]):
    execute_columns = ["created_at", "deleted_at"]

    def __init__(self, session: AsyncSession):
        super().__init__(model=Todo, session=session)
