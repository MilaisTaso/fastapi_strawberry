from typing import Generic, TypeVar

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from src.auth.repositories.user import UserRepository
from src.core.repositories.bases import DatabaseRepository
from src.core.settings.database import get_db_session
from src.todos.repositories.todo import TodoRepository

Repository = TypeVar("Repository", bound=DatabaseRepository)


class AppContext(BaseContext, Generic[Repository]):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


async def get_context(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    if "todo" in request.url.path:
        repository = TodoRepository(session=session)
    else:
        repository = UserRepository(session=session)

    return AppContext(repository=repository)
