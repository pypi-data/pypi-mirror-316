import datetime
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CustomApiIntegrationResponse")


@_attrs_define
class CustomApiIntegrationResponse:
    """Schema for custom API integration response.

    Attributes:
        name (str): Integration name
        type_ (Any): Type of integration
        uuid (UUID): Integration unique identifier
        project_uuid (UUID): Project UUID this integration belongs to
        status (Any): Current integration status
        created_at (datetime.datetime): Integration creation timestamp
        updated_at (datetime.datetime): Last update timestamp
        config (Any): Custom API configuration
    """

    name: str
    type_: Any
    uuid: UUID
    project_uuid: UUID
    status: Any
    created_at: datetime.datetime
    updated_at: datetime.datetime
    config: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        uuid = str(self.uuid)

        project_uuid = str(self.project_uuid)

        status = self.status

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        config = self.config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "uuid": uuid,
                "project_uuid": project_uuid,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type_ = d.pop("type")

        uuid = UUID(d.pop("uuid"))

        project_uuid = UUID(d.pop("project_uuid"))

        status = d.pop("status")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        config = d.pop("config")

        custom_api_integration_response = cls(
            name=name,
            type_=type_,
            uuid=uuid,
            project_uuid=project_uuid,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            config=config,
        )

        custom_api_integration_response.additional_properties = d
        return custom_api_integration_response

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
