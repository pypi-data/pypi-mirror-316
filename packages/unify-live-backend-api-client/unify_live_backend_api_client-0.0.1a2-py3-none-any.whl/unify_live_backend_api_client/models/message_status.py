from enum import Enum


class MessageStatus(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"
    SENDING = "sending"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
