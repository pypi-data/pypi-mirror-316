from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectInviteCreate")


@_attrs_define
class ProjectInviteCreate:
    """Schema for creating a new project invite.

    Attributes:
        email (str): Email of the user to invite
        expires_in_hours (Union[Unset, int]): Number of hours until invite expires Default: 48.
    """

    email: str
    expires_in_hours: Union[Unset, int] = 48
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        expires_in_hours = self.expires_in_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if expires_in_hours is not UNSET:
            field_dict["expires_in_hours"] = expires_in_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        expires_in_hours = d.pop("expires_in_hours", UNSET)

        project_invite_create = cls(
            email=email,
            expires_in_hours=expires_in_hours,
        )

        project_invite_create.additional_properties = d
        return project_invite_create

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
