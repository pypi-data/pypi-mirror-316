from enum import Enum


class WidgetTheme(str, Enum):
    AUTO = "auto"
    DARK = "dark"
    LIGHT = "light"

    def __str__(self) -> str:
        return str(self.value)
