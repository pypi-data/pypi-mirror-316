from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_status import IntegrationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.telegram_integration_config import TelegramIntegrationConfig


T = TypeVar("T", bound="TelegramIntegrationUpdate")


@_attrs_define
class TelegramIntegrationUpdate:
    """Schema for updating a telegram integration.

    Attributes:
        name (Union[None, Unset, str]): New integration name
        status (Union[IntegrationStatus, None, Unset]): New integration status
        config (Union['TelegramIntegrationConfig', None, Unset]): Updated telegram configuration
    """

    name: Union[None, Unset, str] = UNSET
    status: Union[IntegrationStatus, None, Unset] = UNSET
    config: Union["TelegramIntegrationConfig", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.telegram_integration_config import TelegramIntegrationConfig

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, IntegrationStatus):
            status = self.status.value
        else:
            status = self.status

        config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.config, Unset):
            config = UNSET
        elif isinstance(self.config, TelegramIntegrationConfig):
            config = self.config.to_dict()
        else:
            config = self.config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.telegram_integration_config import TelegramIntegrationConfig

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_status(data: object) -> Union[IntegrationStatus, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = IntegrationStatus(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[IntegrationStatus, None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_config(data: object) -> Union["TelegramIntegrationConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = TelegramIntegrationConfig.from_dict(data)

                return config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TelegramIntegrationConfig", None, Unset], data)

        config = _parse_config(d.pop("config", UNSET))

        telegram_integration_update = cls(
            name=name,
            status=status,
            config=config,
        )

        telegram_integration_update.additional_properties = d
        return telegram_integration_update

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
