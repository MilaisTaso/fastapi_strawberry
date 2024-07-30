from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from src.auth.libraries.dependencies import get_repository
from src.auth.libraries.token import ALGORITHM
from src.auth.schemas.token import TokenPayload
from src.core.settings.config import settings
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.users.models.user import User
from src.users.repositories.user import UserRepository

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False,
)


async def get_current_user(
    user_repo: Annotated[UserRepository, Depends(get_repository(UserRepository))],
    token: Annotated[str, Depends(oauth2_bearer)],
) -> User:
    """
    クラスメソッドとして実装するとSecurityに依存関係を注入できないため、
    このディレクトリに単体のメソッドとして定義
    """

    if not token:
        raise AppException(error=ErrorMessage.CouldNotValidateCredentials)

    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET, algorithms=[ALGORITHM])
        token_data: TokenPayload = TokenPayload(sub=payload["sub"])

    except (JWTError, ValidationError, KeyError):
        raise AppException(ErrorMessage.CouldNotValidateCredentials)

    user = await user_repo.get_context_by_id(token_data.sub)
    if not user:
        raise AppException(ErrorMessage.NOT_FOUND("User"))

    return user
