from uuid import UUID

import strawberry

from src.auth.schemas.user import CreateUser, UpdateUser


@strawberry.experimental.pydantic.input(model=CreateUser)
class CreateUserInput:
    first_name: str
    last_name: str
    email: str
    password: str


@strawberry.experimental.pydantic.input(model=UpdateUser)
class UpdateUserInput:
    id: UUID
    first_name: str
    last_name: str
    nick_name: str
    email: str
    password: str
