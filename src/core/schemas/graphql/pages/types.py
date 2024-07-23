import strawberry

from src.core.schemas.enums.sort_direction import SortDirection
from src.core.schemas.pydantic.paginate import PageMeta

SortDirectionType = strawberry.enum(SortDirection, name="Direction")


@strawberry.experimental.pydantic.type(model=PageMeta)
class PageMetaType:
    current_page: int
    total_page_count: int
    total_data_count: int
    per_page: int
