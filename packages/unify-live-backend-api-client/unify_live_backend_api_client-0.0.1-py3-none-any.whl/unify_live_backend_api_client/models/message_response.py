import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_status import MessageStatus
from ..models.message_type import MessageType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_attachment import MessageAttachment


T = TypeVar("T", bound="MessageResponse")


@_attrs_define
class MessageResponse:
    """Schema for message response data.

    Example:
        {'attachments': [], 'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help you
            today?', 'created_at': '2024-01-01T12:00:00Z', 'message_type': 'text', 'participant_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'status': 'delivered', 'updated_at': '2024-01-01T12:00:00Z', 'uuid':
            '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        uuid (UUID): Unique identifier of the message
        chat_uuid (UUID): UUID of the chat this message belongs to
        participant_uuid (UUID): UUID of the message sender
        content (str): Text content of the message
        message_type (MessageType): Available message types in the system.
        status (MessageStatus): Possible message statuses during delivery lifecycle.
        created_at (datetime.datetime): Timestamp when message was created
        updated_at (datetime.datetime): Timestamp when message was last updated
        reply_to_uuid (Union[None, UUID, Unset]): UUID of the message this is a reply to
        external_id (Union[None, Unset, str]): Message ID in external system
        attachments (Union[Unset, list['MessageAttachment']]): List of files attached to this message
    """

    uuid: UUID
    chat_uuid: UUID
    participant_uuid: UUID
    content: str
    message_type: MessageType
    status: MessageStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    reply_to_uuid: Union[None, UUID, Unset] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    attachments: Union[Unset, list["MessageAttachment"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        chat_uuid = str(self.chat_uuid)

        participant_uuid = str(self.participant_uuid)

        content = self.content

        message_type = self.message_type.value

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "chat_uuid": chat_uuid,
                "participant_uuid": participant_uuid,
                "content": content,
                "message_type": message_type,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if reply_to_uuid is not UNSET:
            field_dict["reply_to_uuid"] = reply_to_uuid
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.message_attachment import MessageAttachment

        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        chat_uuid = UUID(d.pop("chat_uuid"))

        participant_uuid = UUID(d.pop("participant_uuid"))

        content = d.pop("content")

        message_type = MessageType(d.pop("message_type"))

        status = MessageStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

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

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = MessageAttachment.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        message_response = cls(
            uuid=uuid,
            chat_uuid=chat_uuid,
            participant_uuid=participant_uuid,
            content=content,
            message_type=message_type,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            reply_to_uuid=reply_to_uuid,
            external_id=external_id,
            attachments=attachments,
        )

        message_response.additional_properties = d
        return message_response

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
