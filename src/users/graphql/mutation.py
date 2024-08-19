import strawberry
from strawberry.types import Info

from src.auth.libraries.decorator import auth_required
from src.core.dependencies import AppContext
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.users.graphql.schemas import DeleteUserInput, UpdateUserInput
from src.users.graphql.types import UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    @auth_required
    async def update_user(
        self, schema: UpdateUserInput, info: Info[AppContext]
    ) -> UserType:
        user_repo = info.context.user_repo
        instance = schema.to_pydantic()

        user = await user_repo.get_context_by_id(instance.id)
        if user is None:
            raise AppException(error=ErrorMessage.NOT_FOUND("User"))

        updated_todo = await user_repo.update(context=user, data=instance)

        return UserType.from_model(updated_todo)

    @strawberry.mutation
    @auth_required
    async def delete_user(self, schema: DeleteUserInput, info: Info[AppContext]) -> str:
        user_repo = info.context.user_repo
        instance = schema.to_pydantic()

        user = await user_repo.get_context_by_id(instance.id)
        if user is None:
            raise AppException(error=ErrorMessage.NOT_FOUND("User"))

        await user_repo.delete(user)

        return f"User: {user.nick_name} is deleted successful."
