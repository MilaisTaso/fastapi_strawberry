import uuid

import strawberry

from src.todos.enums.todo_status import TodoStatus


@strawberry.input
class CreateTodoInput:
    title: str
    description: str


@strawberry.input
class UpdateTodoInput:
    id: uuid.UUID
    title: str | None = None
    description: str | None = None
    status: TodoStatus
