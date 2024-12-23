from enum import Enum


class IntegrationType(str, Enum):
    CUSTOM_API = "custom_api"
    TELEGRAM = "telegram"
    WIDGET = "widget"

    def __str__(self) -> str:
        return str(self.value)
