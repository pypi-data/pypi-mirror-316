from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomApiIntegrationConfig")


@_attrs_define
class CustomApiIntegrationConfig:
    """Schema for custom API integration configuration.

    Attributes:
        endpoint_url (str): Endpoint URL for the custom API
        max_retries (Union[Unset, int]): Maximum number of retry attempts Default: 3.
        retry_interval (Union[Unset, int]): Interval between retries in seconds Default: 60.
        timeout_seconds (Union[Unset, int]): Request timeout in seconds Default: 30.
    """

    endpoint_url: str
    max_retries: Union[Unset, int] = 3
    retry_interval: Union[Unset, int] = 60
    timeout_seconds: Union[Unset, int] = 30
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint_url = self.endpoint_url

        max_retries = self.max_retries

        retry_interval = self.retry_interval

        timeout_seconds = self.timeout_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endpoint_url": endpoint_url,
            }
        )
        if max_retries is not UNSET:
            field_dict["max_retries"] = max_retries
        if retry_interval is not UNSET:
            field_dict["retry_interval"] = retry_interval
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        endpoint_url = d.pop("endpoint_url")

        max_retries = d.pop("max_retries", UNSET)

        retry_interval = d.pop("retry_interval", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        custom_api_integration_config = cls(
            endpoint_url=endpoint_url,
            max_retries=max_retries,
            retry_interval=retry_interval,
            timeout_seconds=timeout_seconds,
        )

        custom_api_integration_config.additional_properties = d
        return custom_api_integration_config

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
