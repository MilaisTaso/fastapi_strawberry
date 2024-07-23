from datetime import datetime
from typing import List, Type
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
    status: Type[TodoStatus] = strawberry.enum(TodoStatus, name="Status")
    updated_at: datetime


@strawberry.type(name="Todos")
class PagedTodoType:
    items: List[TodoType]
    metadata: PageMetaType

    @classmethod
    def from_model(cls, todos: List[Todo], page_meta: PageMeta):
        metadata = PageMetaType.from_pydantic(page_meta)
        todo_list = [TodoType.from_model(todo) for todo in todos]

        return cls(items=todo_list, metadata=metadata)
