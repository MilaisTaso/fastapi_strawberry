import re
import uuid

from pydantic import EmailStr, Field, SecretStr, field_validator

from src.core.schemas.pydantic.base import BasePydanticSchema


class BaseUser(BasePydanticSchema):
    first_name: str = Field(min_length=1, max_length=10)
    last_name: str = Field(min_length=1, max_length=10)
    nick_name: str
    email: EmailStr  # 別途ライブラリが必要だが、勝手にバリデーションしてくれる
    password: SecretStr

    @field_validator("password", mode="before")
    @classmethod
    def check_password(cls, value: str) -> SecretStr:
        assert len(value) >= 8, "Password must be at least 8 characters long"
        assert (
            re.search(r"[A-Z]", value) is None
        ), "Password must contain at least one uppercase letter'"
        assert (
            re.search(r"[a-z]", value) is None
        ), "Password must contain at least one lowercase letter"
        assert (
            re.search(r'[!@#$%^&*(),.?":{}|<>]', value) is None
        ), "Password must contain at least one special character"

        return SecretStr(value)

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        nick_name: str | None = None,
        *args,
        **kwargs,
    ):
        if nick_name is None:
            nick_name = f"{first_name} {last_name}"

        super().__init__(
            first_name=first_name,
            last_name=last_name,
            nick_name=nick_name,
            email=email,
            password=password,
            *args,
            **kwargs,
        )


class CreateUser(BaseUser):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class UpdateUser(BaseUser):
    id: uuid.UUID
    nick_name: str = Field(min_length=2, max_length=20)
