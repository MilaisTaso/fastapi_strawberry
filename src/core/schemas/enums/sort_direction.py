from enum import Enum

import strawberry


@strawberry.enum
class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"
