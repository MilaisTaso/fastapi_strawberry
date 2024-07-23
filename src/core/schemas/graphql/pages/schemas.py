import strawberry

from src.core.schemas.enums.sort_direction import SortDirection
from src.core.schemas.pydantic.paginate import PageQuery

SortType = strawberry.enum(SortDirection, name="SortDirection")


@strawberry.experimental.pydantic.input(model=PageQuery)
class PageQueryInput:
    page: int = strawberry.field(default=1)
    per_page: int = strawberry.field(default=20)
