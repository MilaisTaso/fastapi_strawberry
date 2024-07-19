from fastapi import status
from fastapi.responses import JSONResponse

from src.core.settings.logs.logger import get_logger

logger = get_logger(__name__)


# ミドルウェアで使用しているが @app.exception_handler() でラップして使うこともできる
def internal_server_error_handler(error: Exception):
    logger.error(f"error occurs Exception: {error}")
    err_dict = {
        "id": "INTERNAL_SERVER_ERROR",
        "message": "予期せぬエラーが発生しました 時間をおいて再度お試しください",
        "detail": str(error),
    }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=err_dict
    )
