import uuid

import strawberry
from pydantic import Field, field_validator

from src.core.schemas.base import BaseSchema
from src.todos.enums.todo_status import TodoStatus


class BaseTodo(BaseSchema):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None


@strawberry.input
class CreateTodo(BaseTodo):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: TodoStatus = TodoStatus.PENDING


@strawberry.input
class UpdateTodo(BaseTodo):
    id: uuid.UUID
    title: str | None = None
    status: TodoStatus

    @field_validator("title", mode="before")
    def check_title_len(self, value: str | None = None):
        if value is None:
            return None

        assert len(value) < 2, "Titles must have at least two characters."
        assert len(value) > 100, "Title must be less than 100 characters."

        return value
