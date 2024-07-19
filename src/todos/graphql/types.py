from datetime import datetime

import strawberry

from src.core.schemas.base import BaseSchema
from todos.enums.todo_status import TodoStatus


@strawberry.type(name="todo")
class TodoType(BaseSchema):
    id: strawberry.ID
    title: str
    description: str | None
    status: TodoStatus
    updated_at: datetime
