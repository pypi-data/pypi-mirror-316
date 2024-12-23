from enum import Enum


class ParticipantType(str, Enum):
    CLIENT = "client"
    MANAGER = "manager"

    def __str__(self) -> str:
        return str(self.value)
