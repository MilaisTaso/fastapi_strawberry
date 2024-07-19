import uuid
from typing import List

import strawberry
from strawberry.types import Info

from src.core.dependeny import AppContext
from src.todos.graphql.types import TodoType
from src.todos.repositories.todo import TodoRepository


@strawberry.type
class Query:
    @strawberry.field(name="todos")
    async def get_todos(self, info: Info[AppContext[TodoRepository]]) -> List[TodoType]:
        todo_repo = info.context.repository
        todos = await todo_repo.get_list_context()

        return [TodoType.model_validate(todo) for todo in todos]

    @strawberry.field
    async def get_todo_by_id(
        self, info: Info[AppContext[TodoRepository]], id: uuid.UUID
    ) -> TodoType:
        todo_repo: TodoRepository = info.context.repository
        todo = await todo_repo.get_context_by_id(id)
        if todo is None:
            raise ValueError("Todo not found")
        return TodoType.model_validate(todo)
