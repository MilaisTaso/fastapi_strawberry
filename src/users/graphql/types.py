import strawberry

from src.auth.schemas.token import TokenPayload
from src.core.schemas.graphql.base import BaseGraphSchema
from src.users.models.user import User


@strawberry.type(name="User")
class UserType(BaseGraphSchema[User]):
    first_name: str
    last_name: str
    nick_name: str
    email: str


@strawberry.experimental.pydantic.type(model=TokenPayload)
class TokenType:
    sub: str


@strawberry.type(name="LoginUser")
class LoginUserType:
    user: UserType
    token: TokenType

    @classmethod
    def from_model(cls, data: User, token_schema: TokenPayload):
        user = UserType.from_model(data)
        token = TokenType.from_pydantic(token_schema)

        return cls(user=user, token=token)
