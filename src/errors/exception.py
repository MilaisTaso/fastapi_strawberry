from typing import Any, Dict, Type

from fastapi import HTTPException, status

from src.errors.messages.base import BaseMessage


class AppException(HTTPException):
    """API例外"""

    id: str
    message: str
    detail: str

    def __init__(
        self,
        error: Type[BaseMessage] | BaseMessage,
        headers: Dict[str, Any] | None = None,
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
            status_code=status.HTTP_200_OK, detail=self.message, headers=headers
        )
