from datetime import datetime
from uuid import UUID

import strawberry

from src.core.schemas.graphql.base import BaseGraphSchema
from src.todos.enums.todo_status import TodoStatus
from src.todos.models.todo import Todo


@strawberry.type(name="Todo")
class TodoType(BaseGraphSchema[Todo]):
    id: UUID
    title: str
    description: str | None
    status: TodoStatus
    updated_at: datetime
