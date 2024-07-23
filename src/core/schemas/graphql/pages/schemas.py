from typing import Any

import strawberry

from src.core.schemas.enums.sort_direction import SortDirection
from src.core.schemas.pydantic.paginate import PageQuery, SortQuery

SortType = strawberry.enum(SortDirection, name="SortDirection")


@strawberry.experimental.pydantic.input(model=PageQuery)
class PageQueryInput:
    page: str
    per_page: str


@strawberry.experimental.pydantic.input(model=SortQuery)
class SortQueryInput:
    field: Any
    direction: SortType  # type: ignore
