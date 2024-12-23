from enum import Enum


class ChatStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    CLOSED = "closed"

    def __str__(self) -> str:
        return str(self.value)
