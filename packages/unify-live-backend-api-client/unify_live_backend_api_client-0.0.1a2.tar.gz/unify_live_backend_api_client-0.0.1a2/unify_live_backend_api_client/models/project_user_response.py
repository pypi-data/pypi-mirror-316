import datetime
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ProjectUserResponse")


@_attrs_define
class ProjectUserResponse:
    """Schema for project user data.

    Example:
        {'email': 'user@example.com', 'joined_at': '2024-03-21T12:00:00Z', 'role': 'admin', 'user_uuid':
            '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        user_uuid (UUID): User's unique identifier
        email (str): User's email address
        role (str): User's role in the project (admin or user)
        joined_at (datetime.datetime): When user joined the project
    """

    user_uuid: UUID
    email: str
    role: str
    joined_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid = str(self.user_uuid)

        email = self.email

        role = self.role

        joined_at = self.joined_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
                "email": email,
                "role": role,
                "joined_at": joined_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        user_uuid = UUID(d.pop("user_uuid"))

        email = d.pop("email")

        role = d.pop("role")

        joined_at = isoparse(d.pop("joined_at"))

        project_user_response = cls(
            user_uuid=user_uuid,
            email=email,
            role=role,
            joined_at=joined_at,
        )

        project_user_response.additional_properties = d
        return project_user_response

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
