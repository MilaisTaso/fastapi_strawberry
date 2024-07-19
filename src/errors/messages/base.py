from typing import Any

from starlette import status


class BaseMessage:
    message: str
    detail: str = "リクエストの処理に失敗しました"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, param: Any | None = None) -> None:
        self.param = param

    def __str__(self) -> str:
        return self.__class__.__name__
