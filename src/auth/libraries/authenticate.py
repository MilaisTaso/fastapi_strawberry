from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from src.auth.libraries.token import ALGORITHM
from src.auth.schemas.token import TokenPayload
from src.core.repositories.dependencies import get_repository
from src.core.settings.config import settings
from src.core.settings.logs.logger import get_logger
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.users.models.user import User
from src.users.repositories.user import UserRepository

logger = get_logger(__name__)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False,
)


async def get_current_user(
    user_repo: Annotated[UserRepository, Depends(get_repository(UserRepository))],
    token: str = Depends(oauth2_bearer),
) -> User | None:
    if not token:
        logger.error("Authentication Failed. Token is empty.")
        raise AppException(error=ErrorMessage.AUTHENTICATION_FAILED)

    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET, algorithms=[ALGORITHM])
        token_data: TokenPayload = TokenPayload(sub=payload["sub"])

    except (JWTError, ValidationError, KeyError):
        logger.error("Authentication Failed. Token is invalid.")
        raise AppException(ErrorMessage.AUTHENTICATION_FAILED)

    user = await user_repo.get_context_by_id(token_data.sub)
    if not user:
        logger.error("Authentication Failed. User is not fount.")
        raise AppException(ErrorMessage.NOT_FOUND("User"))

    return user
