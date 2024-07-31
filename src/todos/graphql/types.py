from datetime import datetime
from typing import List
from uuid import UUID

import strawberry

from src.core.schemas.graphql.base import BaseGraphSchema
from src.core.schemas.graphql.pages.types import PageMetaType
from src.core.schemas.pydantic.paginate import PageMeta
from src.todos.enums.todo import TodoStatus
from src.todos.models.todo import Todo


@strawberry.type(name="Todo")
class TodoType(BaseGraphSchema[Todo]):
    id: UUID
    title: str
    description: str | None
    status: TodoStatus
    updated_at: datetime


@strawberry.type(name="Todos")
class PagedTodoType:
    items: List[TodoType] = strawberry.field(default_factory=list)
    metadata: PageMetaType

    @classmethod
    def from_model(cls, todos: List[Todo], page_meta: PageMeta):
        todo_list = [TodoType.from_model(todo) for todo in todos] if todos else []
        metadata = PageMetaType.from_pydantic(page_meta)

        return cls(items=todo_list, metadata=metadata)
