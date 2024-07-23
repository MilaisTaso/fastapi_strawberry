from uuid import UUID

import strawberry

from src.todos.enums.todo_status import TodoStatus
from src.todos.schemas.todo import CreateTodo, UpdateTodo

StatusType = strawberry.enum(TodoStatus, name="Status")


@strawberry.experimental.pydantic.input(model=CreateTodo)
class CreateTodoInput:
    title: str
    description: str


@strawberry.experimental.pydantic.input(model=UpdateTodo)
class UpdateTodoInput:
    id: UUID
    title: str | None = None
    description: str | None = None
    status: StatusType  # type: ignore
