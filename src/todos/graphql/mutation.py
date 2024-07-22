import strawberry
from strawberry.types import Info

from src.core.dependeny import AppContext
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.todos.graphql.schemas import CreateTodoInput, UpdateTodoInput
from src.todos.graphql.types import TodoType
from src.todos.repositories.todo import TodoRepository
from src.todos.schemas.todo import CreateTodo, UpdateTodo


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_todo(
        self, schema: CreateTodoInput, info: Info[AppContext[TodoRepository]]
    ) -> TodoType:
        todo_repo = info.context.repository
        todo = CreateTodo(title=schema.title, description=schema.description)
        new_todo = await todo_repo.create(data=CreateTodo.from_strawberry(schema))

        return TodoType.from_model(new_todo)

    @strawberry.mutation
    async def update_todo(
        self, schema: UpdateTodoInput, info: Info[AppContext[TodoRepository]]
    ) -> TodoType:
        todo_repo = info.context.repository
        todo = await todo_repo.get_context_by_id(schema.id)
        update_todo = UpdateTodo(id=schema.id, title=schema.title, status=schema.status)
        if todo is None:
            raise AppException(error=ErrorMessage.NOT_FOUND("Todo"))
        updated_todo = await todo_repo.update(context=todo, data=update_todo)

        return TodoType.from_model(updated_todo)
