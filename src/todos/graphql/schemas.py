from uuid import UUID

import strawberry

from src.core.schemas.enums.sort_direction import SortDirection
from src.todos.enums.todo import TodoSortField, TodoStatus
from src.todos.schemas.todo import CreateTodo, DeleteTodo, TodoSortQuery, UpdateTodo


@strawberry.experimental.pydantic.input(model=CreateTodo)
class CreateTodoInput:
    title: str
    description: str


@strawberry.experimental.pydantic.input(model=UpdateTodo)
class UpdateTodoInput:
    id: UUID
    title: str | None = None
    description: str | None = None
    status: TodoStatus  # type: ignore


@strawberry.experimental.pydantic.input(model=DeleteTodo)
class DeleteTodoInput:
    id: UUID


@strawberry.experimental.pydantic.input(model=TodoSortQuery)
class TodoSortQueryInput:
    field: TodoSortField = strawberry.field(default=TodoSortField.TITLE)  # type: ignore
    direction: SortDirection = strawberry.field(default=SortDirection.ASC)  # type: ignore
