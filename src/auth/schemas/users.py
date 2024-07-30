import uuid

from pydantic import EmailStr, Field

from src.auth.schemas.token import TokenPayload
from src.core.schemas.pydantic.base import BasePydanticSchema
from src.users.schemas.user import BaseUser


class SignUpUser(BaseUser):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class LoginUser(BasePydanticSchema):
    email: EmailStr
    password: str


class UserResponse(BasePydanticSchema):
    first_name: str
    last_name: str
    nick_name: str
    email: str


class LoginUserResponse(BasePydanticSchema):
    user: UserResponse
    token: TokenPayload
