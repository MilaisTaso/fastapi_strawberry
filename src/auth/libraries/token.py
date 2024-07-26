from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from src.core.settings.config import settings

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

"""パスワード関係"""


# 渡されたパスワードが同一のものかチェックする
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


# ハッシュ化したパスワードの生成
def hashed_convert(string: str) -> str:
    return bcrypt_context.hash(string)


"""認証関係"""


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    # トークンを作る際にidというフィールドも設定できる
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET, algorithm=ALGORITHM)

    return encoded_jwt
