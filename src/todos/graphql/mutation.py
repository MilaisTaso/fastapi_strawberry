import strawberry
from strawberry.types import Info

from src.core.dependencies import AppContext
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.todos.graphql.schemas import CreateTodoInput, UpdateTodoInput
from src.todos.graphql.types import TodoType


@strawberry.type
class TodoMutation:
    @strawberry.mutation
    async def create_todo(
        self, schema: CreateTodoInput, info: Info[AppContext]
    ) -> TodoType:
        todo_repo = info.context.todo_repo
        new_todo = await todo_repo.create(data=schema.to_pydantic())

        return TodoType.from_model(new_todo)

    @strawberry.mutation
    async def update_todo(
        self, schema: UpdateTodoInput, info: Info[AppContext]
    ) -> TodoType:
        todo_repo = info.context.todo_repo
        instance = schema.to_pydantic()

        todo = await todo_repo.get_context_by_id(instance.id)
        if todo is None:
            raise AppException(error=ErrorMessage.NOT_FOUND("Todo"))

        updated_todo = await todo_repo.update(context=todo, data=instance)

        return TodoType.from_model(updated_todo)
