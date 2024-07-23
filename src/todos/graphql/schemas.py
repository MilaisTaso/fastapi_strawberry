from typing import Type
from uuid import UUID

import strawberry

from src.core.schemas.graphql.pages.types import SortDirectionType
from src.todos.enums.todo import TodoStatus
from src.todos.schemas.todo import CreateTodo, TodoSortQuery, UpdateTodo
from todos.enums.todo import TodoSortField

StatusType = strawberry.enum(TodoStatus, name="Status")
TodoSortFieldType = strawberry.enum(TodoSortField, name="Field")


@strawberry.experimental.pydantic.input(model=CreateTodo)
class CreateTodoInput:
    title: str
    description: str


@strawberry.experimental.pydantic.input(model=UpdateTodo)
class UpdateTodoInput:
    id: UUID
    title: str | None = None
    description: str | None = None
    status: Type[StatusType]  # type: ignore


@strawberry.experimental.pydantic.input(model=TodoSortQuery)
class TodoSortQueryInput:
    field: Type[TodoSortFieldType] = strawberry.field(default=TodoSortFieldType.TITLE)  # type: ignore
    direction: Type[SortDirectionType] = strawberry.field(default=SortDirectionType.ASC)  # type: ignore
