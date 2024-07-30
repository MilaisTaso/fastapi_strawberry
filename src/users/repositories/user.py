from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas.users import SignUpUser
from src.core.repositories.bases import DatabaseRepository
from src.users.models.user import User
from src.users.schemas.user import UpdateUser


class UserRepository(DatabaseRepository[User, SignUpUser, UpdateUser]):
    exclude_columns = ["created_at", "deleted_at"]

    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
