from enum import Enum

import strawberry


@strawberry.enum
class TodoStatus(Enum):
    PENDING = "Pending"
    DOING = "Dding"
    DONE = "Done"
