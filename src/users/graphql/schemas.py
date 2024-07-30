from uuid import UUID

import strawberry

from src.users.schemas.user import UpdateUser


@strawberry.experimental.pydantic.input(model=UpdateUser)
class UpdateUserInput:
    id: UUID
    first_name: str
    last_name: str
    nick_name: str
    email: str
    password: str
