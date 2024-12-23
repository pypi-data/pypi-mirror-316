import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlockStatus")


@_attrs_define
class BlockStatus:
    """Schema for client block status.

    Example:
        {'blocked_at': '2024-01-01T12:00:00Z', 'expires_at': '2024-02-01T00:00:00Z', 'is_blocked': True, 'reason': 'Spam
            messages'}

    Attributes:
        is_blocked (bool): Whether client is currently blocked
        reason (Union[None, Unset, str]): Current block reason
        blocked_at (Union[None, Unset, datetime.datetime]): When client was blocked
        expires_at (Union[None, Unset, datetime.datetime]): When block expires
    """

    is_blocked: bool
    reason: Union[None, Unset, str] = UNSET
    blocked_at: Union[None, Unset, datetime.datetime] = UNSET
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_blocked = self.is_blocked

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        blocked_at: Union[None, Unset, str]
        if isinstance(self.blocked_at, Unset):
            blocked_at = UNSET
        elif isinstance(self.blocked_at, datetime.datetime):
            blocked_at = self.blocked_at.isoformat()
        else:
            blocked_at = self.blocked_at

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_blocked": is_blocked,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if blocked_at is not UNSET:
            field_dict["blocked_at"] = blocked_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        is_blocked = d.pop("is_blocked")

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_blocked_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                blocked_at_type_0 = isoparse(data)

                return blocked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        blocked_at = _parse_blocked_at(d.pop("blocked_at", UNSET))

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        block_status = cls(
            is_blocked=is_blocked,
            reason=reason,
            blocked_at=blocked_at,
            expires_at=expires_at,
        )

        block_status.additional_properties = d
        return block_status

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
