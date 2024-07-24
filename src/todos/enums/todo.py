from enum import Enum

import strawberry


@strawberry.enum
class TodoStatus(Enum):
    PENDING = "Pending"
    DOING = "Doing"
    DONE = "Done"


@strawberry.enum
class TodoSortField(Enum):
    TITLE = "title"
    CREATED_AT = "created_at"
