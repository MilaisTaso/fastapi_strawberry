import strawberry
from strawberry.types import Info

from src.auth.libraries.decorator import auth_required
from src.core.dependencies import AppContext
from src.core.settings.logs.logger import get_logger
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.users.graphql.types import UserType

logger = get_logger(__name__)


@strawberry.type
class UserQuery:
    @strawberry.field(name="me")
    @auth_required
    async def get_me(self, info: Info[AppContext]) -> UserType:
        user = info.context.user

        if user is None:
            raise AppException(error=ErrorMessage.NOT_FOUND("User"))

        return UserType.from_model(user)
