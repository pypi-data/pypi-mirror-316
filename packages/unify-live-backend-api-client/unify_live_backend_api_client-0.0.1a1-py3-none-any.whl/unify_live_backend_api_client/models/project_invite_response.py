import datetime
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ProjectInviteResponse")


@_attrs_define
class ProjectInviteResponse:
    """Schema for project invite response data.

    Example:
        {'created_at': '2024-01-01T10:00:00Z', 'email': 'user@example.com', 'expires_at': '2024-01-01T12:00:00Z',
            'project_uuid': '123e4567-e89b-12d3-a456-426614174000', 'status': 'pending', 'uuid':
            '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        uuid (UUID): Unique identifier of the invite
        project_uuid (UUID): Project UUID
        email (str): Invited user's email
        status (str): Current invite status
        expires_at (datetime.datetime): When invite expires
        created_at (datetime.datetime): When invite was created
    """

    uuid: UUID
    project_uuid: UUID
    email: str
    status: str
    expires_at: datetime.datetime
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        project_uuid = str(self.project_uuid)

        email = self.email

        status = self.status

        expires_at = self.expires_at.isoformat()

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "project_uuid": project_uuid,
                "email": email,
                "status": status,
                "expires_at": expires_at,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        project_uuid = UUID(d.pop("project_uuid"))

        email = d.pop("email")

        status = d.pop("status")

        expires_at = isoparse(d.pop("expires_at"))

        created_at = isoparse(d.pop("created_at"))

        project_invite_response = cls(
            uuid=uuid,
            project_uuid=project_uuid,
            email=email,
            status=status,
            expires_at=expires_at,
            created_at=created_at,
        )

        project_invite_response.additional_properties = d
        return project_invite_response

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
