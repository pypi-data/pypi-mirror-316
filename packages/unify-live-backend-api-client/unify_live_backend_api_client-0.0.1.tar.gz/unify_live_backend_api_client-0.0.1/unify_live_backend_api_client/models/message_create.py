from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageCreate")


@_attrs_define
class MessageCreate:
    """Schema for creating a new message in the system.

    Example:
        {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help you today?',
            'message_type': 'text'}

    Attributes:
        chat_uuid (UUID): UUID of the chat where message should be sent
        content (str): Text content of the message
        message_type (Union[Unset, Any]): Type of the message (text or file) Default: 'text'.
        reply_to_uuid (Union[None, UUID, Unset]): UUID of the message being replied to
        external_id (Union[None, Unset, str]): Message ID in external system (e.g., Telegram message ID)
    """

    chat_uuid: UUID
    content: str
    message_type: Union[Unset, Any] = "text"
    reply_to_uuid: Union[None, UUID, Unset] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chat_uuid = str(self.chat_uuid)

        content = self.content

        message_type = self.message_type

        reply_to_uuid: Union[None, Unset, str]
        if isinstance(self.reply_to_uuid, Unset):
            reply_to_uuid = UNSET
        elif isinstance(self.reply_to_uuid, UUID):
            reply_to_uuid = str(self.reply_to_uuid)
        else:
            reply_to_uuid = self.reply_to_uuid

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat_uuid": chat_uuid,
                "content": content,
            }
        )
        if message_type is not UNSET:
            field_dict["message_type"] = message_type
        if reply_to_uuid is not UNSET:
            field_dict["reply_to_uuid"] = reply_to_uuid
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        chat_uuid = UUID(d.pop("chat_uuid"))

        content = d.pop("content")

        message_type = d.pop("message_type", UNSET)

        def _parse_reply_to_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reply_to_uuid_type_0 = UUID(data)

                return reply_to_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        reply_to_uuid = _parse_reply_to_uuid(d.pop("reply_to_uuid", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        message_create = cls(
            chat_uuid=chat_uuid,
            content=content,
            message_type=message_type,
            reply_to_uuid=reply_to_uuid,
            external_id=external_id,
        )

        message_create.additional_properties = d
        return message_create

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
