from enum import Enum


class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
