import datetime
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClientResponse")


@_attrs_define
class ClientResponse:
    """Schema for client response data.

    Attributes:
        uuid (UUID): Client UUID
        integration_uuid (UUID): Integration UUID
        external_id (str): External system ID
        is_online (bool): Online status
        created_at (datetime.datetime): Creation timestamp
        updated_at (datetime.datetime): Last update timestamp
        first_name (Union[None, Unset, str]): First name
        last_name (Union[None, Unset, str]): Last name
        email (Union[None, Unset, str]): Email
        phone (Union[None, Unset, str]): Phone number
        last_seen_at (Union[None, Unset, datetime.datetime]): Last activity timestamp
    """

    uuid: UUID
    integration_uuid: UUID
    external_id: str
    is_online: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    first_name: Union[None, Unset, str] = UNSET
    last_name: Union[None, Unset, str] = UNSET
    email: Union[None, Unset, str] = UNSET
    phone: Union[None, Unset, str] = UNSET
    last_seen_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        integration_uuid = str(self.integration_uuid)

        external_id = self.external_id

        is_online = self.is_online

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        last_seen_at: Union[None, Unset, str]
        if isinstance(self.last_seen_at, Unset):
            last_seen_at = UNSET
        elif isinstance(self.last_seen_at, datetime.datetime):
            last_seen_at = self.last_seen_at.isoformat()
        else:
            last_seen_at = self.last_seen_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "integration_uuid": integration_uuid,
                "external_id": external_id,
                "is_online": is_online,
                "created_at": created_at,
                "updated_at": updated_at,
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
        if last_seen_at is not UNSET:
            field_dict["last_seen_at"] = last_seen_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        integration_uuid = UUID(d.pop("integration_uuid"))

        external_id = d.pop("external_id")

        is_online = d.pop("is_online")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

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

        def _parse_last_seen_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_at_type_0 = isoparse(data)

                return last_seen_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_seen_at = _parse_last_seen_at(d.pop("last_seen_at", UNSET))

        client_response = cls(
            uuid=uuid,
            integration_uuid=integration_uuid,
            external_id=external_id,
            is_online=is_online,
            created_at=created_at,
            updated_at=updated_at,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            last_seen_at=last_seen_at,
        )

        client_response.additional_properties = d
        return client_response

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
