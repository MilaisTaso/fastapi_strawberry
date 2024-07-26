from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.user import User
from src.auth.schemas.user import CreateUser, UpdateUser
from src.core.repositories.bases import DatabaseRepository


class UserRepository(DatabaseRepository[User, CreateUser, UpdateUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
