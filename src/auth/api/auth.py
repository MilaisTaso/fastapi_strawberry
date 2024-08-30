from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.libraries.token import create_access_token, verify_password
from src.auth.schemas.users import LoginUserResponse, SignUpUser, UserResponse, LoginUser
from src.core.repositories.dependencies import get_repository
from src.core.settings.logs.logger import get_logger
from src.errors.exception import AppException
from src.errors.messages.error_message import ErrorMessage
from src.users.models.user import User
from src.users.repositories.user import UserRepository

logger = get_logger(__name__)

router = APIRouter(tags=["Auth"])
DependsUser = Annotated[UserRepository, Depends(get_repository(UserRepository))]


@router.post("/signup")
async def signup(user_repo: DependsUser, request: SignUpUser = Body()):
    exist_user = await user_repo.get_context(User.email == request.email)
    if exist_user is not None:
        raise AppException(error=ErrorMessage.ENTITY_ALREADY_EXISTS("USER"))

    new_user = await user_repo.create(data=request)
    user = UserResponse(
        nick_name=new_user.nick_name,
        email=new_user.email,
    )

    access_token = create_access_token(new_user.id)

    return LoginUserResponse(user=user, token=access_token)


@router.post("/login")
async def login(user_repo: DependsUser, form: LoginUser = Body()):
    logger.info(f"ログイン リクエスト: {form}")
    exist_user = await user_repo.get_context(User.email == form.username)
    if exist_user is None:
        raise AppException(error=ErrorMessage.NOT_FOUND("USER"))

    if not verify_password(form.password, exist_user.password):
        raise AppException(error=ErrorMessage.WRONG_PASSWORD)

    user = UserResponse(
        nick_name=exist_user.nick_name,
        email=exist_user.email,
    )

    access_token = create_access_token(exist_user.id)

    return LoginUserResponse(user=user, token=access_token)
