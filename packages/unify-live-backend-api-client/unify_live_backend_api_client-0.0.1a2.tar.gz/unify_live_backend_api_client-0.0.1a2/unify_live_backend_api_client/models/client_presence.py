import datetime
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClientPresence")


@_attrs_define
class ClientPresence:
    """Schema for client presence status.

    Attributes:
        is_online (bool): Whether client is currently online
        last_seen_at (Union[None, Unset, datetime.datetime]): When client was last active
        current_chat_uuid (Union[None, UUID, Unset]): Current active chat UUID
    """

    is_online: bool
    last_seen_at: Union[None, Unset, datetime.datetime] = UNSET
    current_chat_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_online = self.is_online

        last_seen_at: Union[None, Unset, str]
        if isinstance(self.last_seen_at, Unset):
            last_seen_at = UNSET
        elif isinstance(self.last_seen_at, datetime.datetime):
            last_seen_at = self.last_seen_at.isoformat()
        else:
            last_seen_at = self.last_seen_at

        current_chat_uuid: Union[None, Unset, str]
        if isinstance(self.current_chat_uuid, Unset):
            current_chat_uuid = UNSET
        elif isinstance(self.current_chat_uuid, UUID):
            current_chat_uuid = str(self.current_chat_uuid)
        else:
            current_chat_uuid = self.current_chat_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_online": is_online,
            }
        )
        if last_seen_at is not UNSET:
            field_dict["last_seen_at"] = last_seen_at
        if current_chat_uuid is not UNSET:
            field_dict["current_chat_uuid"] = current_chat_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        is_online = d.pop("is_online")

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

        def _parse_current_chat_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_chat_uuid_type_0 = UUID(data)

                return current_chat_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        current_chat_uuid = _parse_current_chat_uuid(d.pop("current_chat_uuid", UNSET))

        client_presence = cls(
            is_online=is_online,
            last_seen_at=last_seen_at,
            current_chat_uuid=current_chat_uuid,
        )

        client_presence.additional_properties = d
        return client_presence

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
