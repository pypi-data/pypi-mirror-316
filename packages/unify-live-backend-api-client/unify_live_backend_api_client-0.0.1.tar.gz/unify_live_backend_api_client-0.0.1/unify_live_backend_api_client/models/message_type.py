from enum import Enum


class MessageType(str, Enum):
    FILE = "file"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
