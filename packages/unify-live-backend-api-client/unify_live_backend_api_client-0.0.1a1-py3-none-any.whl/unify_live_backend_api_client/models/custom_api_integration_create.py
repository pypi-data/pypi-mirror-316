from typing import Any, Literal, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomApiIntegrationCreate")


@_attrs_define
class CustomApiIntegrationCreate:
    """Schema for creating a new custom API integration.

    Attributes:
        name (str): Integration name
        project_uuid (UUID): Project UUID this integration belongs to
        config (Any): Custom API configuration
        type_ (Union[Literal['custom_api'], Unset]): Must be 'custom_api' Default: 'custom_api'.
    """

    name: str
    project_uuid: UUID
    config: Any
    type_: Union[Literal["custom_api"], Unset] = "custom_api"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_uuid = str(self.project_uuid)

        config = self.config

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "project_uuid": project_uuid,
                "config": config,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        project_uuid = UUID(d.pop("project_uuid"))

        config = d.pop("config")

        type_ = cast(Union[Literal["custom_api"], Unset], d.pop("type", UNSET))
        if type_ != "custom_api" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'custom_api', got '{type_}'")

        custom_api_integration_create = cls(
            name=name,
            project_uuid=project_uuid,
            config=config,
            type_=type_,
        )

        custom_api_integration_create.additional_properties = d
        return custom_api_integration_create

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
