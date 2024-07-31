from functools import wraps
from typing import Any, Awaitable, Callable

from src.core.dependencies import AppContext
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage


def auth_required(func: Callable[..., Awaitable[Any]]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info: AppContext | None = kwargs.get("info")
        if info is None:
            raise TypeError("Missing argument 'info' in func")

        if info.context.user is None:
            raise AppException(error=ErrorMessage.AUTHENTICATION_FAILED)

        return await func(*args, **kwargs)

    return wrapper
