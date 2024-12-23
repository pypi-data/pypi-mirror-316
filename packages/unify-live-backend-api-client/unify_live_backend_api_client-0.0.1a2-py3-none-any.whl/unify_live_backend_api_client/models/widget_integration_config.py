from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.widget_theme import WidgetTheme
from ..types import UNSET, Unset

T = TypeVar("T", bound="WidgetIntegrationConfig")


@_attrs_define
class WidgetIntegrationConfig:
    """Schema for widget integration configuration.

    Attributes:
        allowed_domain (str): List of domains where widget can be embedded
        chat_window_title (str): Title of the chat window
        widget_theme (Union[None, Unset, WidgetTheme]): Widget theme preference
        welcome_message (Union[None, Unset, str]): Welcome message shown when widget opens
    """

    allowed_domain: str
    chat_window_title: str
    widget_theme: Union[None, Unset, WidgetTheme] = UNSET
    welcome_message: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_domain = self.allowed_domain

        chat_window_title = self.chat_window_title

        widget_theme: Union[None, Unset, str]
        if isinstance(self.widget_theme, Unset):
            widget_theme = UNSET
        elif isinstance(self.widget_theme, WidgetTheme):
            widget_theme = self.widget_theme.value
        else:
            widget_theme = self.widget_theme

        welcome_message: Union[None, Unset, str]
        if isinstance(self.welcome_message, Unset):
            welcome_message = UNSET
        else:
            welcome_message = self.welcome_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed_domain": allowed_domain,
                "chat_window_title": chat_window_title,
            }
        )
        if widget_theme is not UNSET:
            field_dict["widget_theme"] = widget_theme
        if welcome_message is not UNSET:
            field_dict["welcome_message"] = welcome_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        allowed_domain = d.pop("allowed_domain")

        chat_window_title = d.pop("chat_window_title")

        def _parse_widget_theme(data: object) -> Union[None, Unset, WidgetTheme]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                widget_theme_type_0 = WidgetTheme(data)

                return widget_theme_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WidgetTheme], data)

        widget_theme = _parse_widget_theme(d.pop("widget_theme", UNSET))

        def _parse_welcome_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        welcome_message = _parse_welcome_message(d.pop("welcome_message", UNSET))

        widget_integration_config = cls(
            allowed_domain=allowed_domain,
            chat_window_title=chat_window_title,
            widget_theme=widget_theme,
            welcome_message=welcome_message,
        )

        widget_integration_config.additional_properties = d
        return widget_integration_config

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
