import uuid

import strawberry
from strawberry.types import Info

from src.core.dependeny import AppContext
from src.core.schemas.graphql.pages.schemas import PageQueryInput
from src.todos.graphql.schemas import TodoSortQueryInput
from src.todos.graphql.types import PagedTodoType, TodoType
from src.todos.repositories.todo import TodoRepository


@strawberry.type
class Query:
    @strawberry.field(name="todos")
    async def get_todos(
        self,
        page_query: PageQueryInput,
        sort_query: TodoSortQueryInput,
        info: Info[AppContext[TodoRepository]],
    ) -> PagedTodoType:
        todo_repo = info.context.repository
        todos, page_mage = await todo_repo.get_paged_context(
            page_query=page_query.to_pydantic(), sort_query=sort_query.to_pydantic()
        )

        return PagedTodoType.from_model(todos=todos, page_meta=page_mage)

    @strawberry.field(name="todo")
    async def get_todo_by_id(
        self, info: Info[AppContext[TodoRepository]], id: uuid.UUID
    ) -> TodoType:
        todo_repo: TodoRepository = info.context.repository
        todo = await todo_repo.get_context_by_id(id)
        if todo is None:
            raise ValueError("Todo not found")
        return TodoType.from_model(todo)
