import re
import uuid
from typing import Any, Dict

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
    field_serializer,
    field_validator,
    model_validator,
)

from src.auth.libraries.token import hashed_convert
from src.core.schemas.pydantic.base import BasePydanticSchema


class BaseUser(BasePydanticSchema):
    nick_name: str = Field(min_length=1, max_length=12)
    email: EmailStr  # 別途ライブラリが必要だが、勝手にバリデーションしてくれる
    password: SecretStr

    @field_serializer("password")
    def dump_by_secret(self, value: SecretStr) -> str:
        return hashed_convert(value.get_secret_value())

    @field_validator("password", mode="before")
    @classmethod
    def check_password(cls, value: str) -> SecretStr:
        assert len(value) >= 8, "Password must be at least 8 characters long"
        assert (
            re.search(r"[A-Z]", value) is not None
        ), "Password must contain at least one uppercase letter'"
        assert (
            re.search(r"[a-z]", value) is not None
        ), "Password must contain at least one lowercase letter"
        assert (
            re.search(r'[!@#$%^&*(),.?":{}|<>]', value) is not None
        ), "Password must contain at least one special character"

        return SecretStr(value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UpdateUser(BaseUser):
    id: uuid.UUID
    nick_name: str = Field(min_length=2, max_length=20)


class DeleteUser(BasePydanticSchema):
    id: uuid.UUID
