import uuid

from pydantic import Field, field_validator

from src.core.schemas.pydantic.base import BasePydanticSchema
from src.todos.enums.todo_status import TodoStatus


class BaseTodo(BasePydanticSchema):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None


class CreateTodo(BaseTodo):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class UpdateTodo(BaseTodo):
    id: uuid.UUID
    title: str | None = None
    description: str | None = None
    status: TodoStatus

    @field_validator("title")
    @classmethod
    def check_title_len(cls, value: str | None):
        if value is None:
            return None

        assert len(value) > 1, "Titles must be at least two characters long."
        assert len(value) <= 100, "Title must be less than 100 characters."
