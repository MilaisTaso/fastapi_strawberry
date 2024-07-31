from fastapi import Depends, Request
from strawberry.fastapi import BaseContext

from src.auth.libraries.authenticate import get_current_user
from src.core.repositories.dependencies import get_repository
from src.todos.repositories.todo import TodoRepository
from src.users.models.user import User
from src.users.repositories.user import UserRepository


class AppContext(BaseContext):
    def __init__(
        self,
        todo_repo: TodoRepository,
        user_repo: UserRepository,
        user: User | None = None,
    ) -> None:
        self.todo_repo = todo_repo
        self.user_repo = user_repo
        self.user = user


async def get_context(
    request: Request,
    todo_repo: TodoRepository = Depends(get_repository(TodoRepository)),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    auth_header = request.headers.get("Authorization")
    if auth_header is not None:
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        user = await get_current_user(token=token, user_repo=user_repo)
    else:
        user = None

    return AppContext(todo_repo=todo_repo, user_repo=user_repo, user=user)
