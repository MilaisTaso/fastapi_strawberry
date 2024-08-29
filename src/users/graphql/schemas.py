from uuid import UUID

import strawberry

from src.users.schemas.user import DeleteUser, UpdateUser


@strawberry.experimental.pydantic.input(model=UpdateUser)
class UpdateUserInput:
    id: UUID
    nick_name: str
    email: str
    password: str


@strawberry.experimental.pydantic.input(model=DeleteUser)
class DeleteUserInput:
    id: UUID
