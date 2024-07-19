from typing import Any, Type

from fastapi import HTTPException, status

from src.errors.messages.base import BaseMessage


class AppException(HTTPException):
    """API例外"""

    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        error: Type[BaseMessage] | BaseMessage,
        headers: dict[str, Any] | None = None,
        detail: Any | None = None,
    ) -> None:
        if isinstance(error, type) and issubclass(error, BaseMessage):
            error_obj = error()
        else:
            error_obj = error

        try:
            parm = getattr(error_obj, "param")
            message = error_obj.message.format(parm)
        except Exception:
            message = error_obj.message

        self.id = str(error_obj)
        self.message = message

        if detail is not None:
            detail = error_obj.detail

        super().__init__(
            status_code=error_obj.status_code, detail=detail, headers=headers
        )
