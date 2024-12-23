from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClientCreate")


@_attrs_define
class ClientCreate:
    """Schema for creating a new client.

    Example:
        {'email': 'john@example.com', 'external_id': 'telegram123456', 'first_name': 'John', 'integration_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'last_name': 'Doe', 'phone': '+1234567890'}

    Attributes:
        integration_uuid (UUID): Integration UUID
        external_id (str): Client ID in external system
        first_name (Union[None, Unset, str]): First name
        last_name (Union[None, Unset, str]): Last name
        email (Union[None, Unset, str]): Email address
        phone (Union[None, Unset, str]): Phone number
    """

    integration_uuid: UUID
    external_id: str
    first_name: Union[None, Unset, str] = UNSET
    last_name: Union[None, Unset, str] = UNSET
    email: Union[None, Unset, str] = UNSET
    phone: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration_uuid = str(self.integration_uuid)

        external_id = self.external_id

        first_name: Union[None, Unset, str]
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: Union[None, Unset, str]
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        email: Union[None, Unset, str]
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        phone: Union[None, Unset, str]
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "integration_uuid": integration_uuid,
                "external_id": external_id,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if phone is not UNSET:
            field_dict["phone"] = phone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        integration_uuid = UUID(d.pop("integration_uuid"))

        external_id = d.pop("external_id")

        def _parse_first_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_phone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone = _parse_phone(d.pop("phone", UNSET))

        client_create = cls(
            integration_uuid=integration_uuid,
            external_id=external_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )

        client_create.additional_properties = d
        return client_create

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
