from typing import Any

from fastapi import Query
from pydantic import field_validator
from sqlalchemy import desc

from src.core.schemas.enums.sort_direction import SortDirection
from src.core.schemas.pydantic.base import BasePydanticSchema


class PageMeta(BasePydanticSchema):
    current_page: int
    total_page_count: int
    total_data_count: int
    per_page: int


class PageQuery(BasePydanticSchema):
    page: int = Query(1)
    per_page: int = Query(20)

    @field_validator("page", mode="before")
    def validate_page(cls, v: int | None = None) -> int:
        value = v if v is not None else 1

        return 1 if value <= 1 else value

    @field_validator("per_page", mode="before")
    def validate_per_page(cls, v: int | None = None) -> int:
        value = v if v is not None else 1
        return 20 if value <= 1 else value

    def get_offset(self) -> int:
        return (
            (self.page - 1) * self.per_page
            if self.page >= 1 and self.per_page >= 1
            else 0
        )

    def apply_to_query(self, query: Any) -> Any:
        offset = self.get_offset()
        return query.offset(offset).limit(self.per_page)


class SortQuery(BasePydanticSchema):
    field: Any | None = Query(None)
    direction: SortDirection = Query(SortDirection.ASC)

    def apply_to_query(self, query: Any, order_by_clause: Any | None = None) -> Any:
        if not order_by_clause:
            return query

        if self.direction == SortDirection.DESC:
            return query.order_by(desc(order_by_clause))
        else:
            return query.order_by(order_by_clause)
