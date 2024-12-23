from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """Schema for user response data.

    Example:
        {'email': 'user@example.com', 'mobile_number': '+1234567890', 'uuid': '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        uuid (UUID): Unique identifier of the user
        email (str): User's email address
        mobile_number (Union[None, Unset, str]): User's mobile phone number
    """

    uuid: UUID
    email: str
    mobile_number: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        email = self.email

        mobile_number: Union[None, Unset, str]
        if isinstance(self.mobile_number, Unset):
            mobile_number = UNSET
        else:
            mobile_number = self.mobile_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "email": email,
            }
        )
        if mobile_number is not UNSET:
            field_dict["mobile_number"] = mobile_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        email = d.pop("email")

        def _parse_mobile_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mobile_number = _parse_mobile_number(d.pop("mobile_number", UNSET))

        user_response = cls(
            uuid=uuid,
            email=email,
            mobile_number=mobile_number,
        )

        user_response.additional_properties = d
        return user_response

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
