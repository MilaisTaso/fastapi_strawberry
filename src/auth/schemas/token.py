from src.core.schemas.pydantic.base import BasePydanticSchema


class TokenPayload(BasePydanticSchema):
    sub: str
