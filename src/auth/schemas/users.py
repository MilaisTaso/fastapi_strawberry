from src.auth.schemas.token import TokenPayload
from src.core.schemas.pydantic.base import BasePydanticSchema
from src.users.schemas.user import BaseUser


class SignUpUser(BaseUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserResponse(BasePydanticSchema):
    first_name: str
    last_name: str
    nick_name: str
    email: str


class LoginUserResponse(BasePydanticSchema):
    user: UserResponse
    token: TokenPayload
