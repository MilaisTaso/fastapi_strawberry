from enum import Enum


class TodoStatus(Enum):
    PENDING = "Pending"
    DOING = "Doing"
    DONE = "Done"


class TodoSortField(Enum):
    TITLE = "title"
    CREATED_AT = "created_at"
