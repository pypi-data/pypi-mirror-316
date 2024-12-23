import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.chat_status import ChatStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.participant_response import ParticipantResponse


T = TypeVar("T", bound="ChatWithParticipants")


@_attrs_define
class ChatWithParticipants:
    """Extended chat response including participant.

    Example:
        {'created_at': '2024-01-01T12:00:00Z', 'description': 'General support discussion', 'integration_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'last_message_at': '2024-01-01T12:00:00Z', 'status': 'active', 'title':
            'Support Chat', 'updated_at': '2024-01-01T12:00:00Z', 'uuid': '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        uuid (UUID): Chat UUID
        integration_uuid (UUID): Integration UUID this chat belongs to
        status (ChatStatus): Available chat statuses.
        created_at (datetime.datetime): When chat was created
        updated_at (datetime.datetime): When chat was last updated
        title (Union[None, Unset, str]): Chat title
        description (Union[None, Unset, str]): Chat description
        first_response_at (Union[None, Unset, datetime.datetime]): When first response was sent
        last_message_at (Union[None, Unset, datetime.datetime]): When last message was sent
        participants (Union[Unset, list['ParticipantResponse']]): List of chat participant
    """

    uuid: UUID
    integration_uuid: UUID
    status: ChatStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    first_response_at: Union[None, Unset, datetime.datetime] = UNSET
    last_message_at: Union[None, Unset, datetime.datetime] = UNSET
    participants: Union[Unset, list["ParticipantResponse"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        integration_uuid = str(self.integration_uuid)

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        first_response_at: Union[None, Unset, str]
        if isinstance(self.first_response_at, Unset):
            first_response_at = UNSET
        elif isinstance(self.first_response_at, datetime.datetime):
            first_response_at = self.first_response_at.isoformat()
        else:
            first_response_at = self.first_response_at

        last_message_at: Union[None, Unset, str]
        if isinstance(self.last_message_at, Unset):
            last_message_at = UNSET
        elif isinstance(self.last_message_at, datetime.datetime):
            last_message_at = self.last_message_at.isoformat()
        else:
            last_message_at = self.last_message_at

        participants: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.participants, Unset):
            participants = []
            for participants_item_data in self.participants:
                participants_item = participants_item_data.to_dict()
                participants.append(participants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "integration_uuid": integration_uuid,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if first_response_at is not UNSET:
            field_dict["first_response_at"] = first_response_at
        if last_message_at is not UNSET:
            field_dict["last_message_at"] = last_message_at
        if participants is not UNSET:
            field_dict["participants"] = participants

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.participant_response import ParticipantResponse

        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        integration_uuid = UUID(d.pop("integration_uuid"))

        status = ChatStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_first_response_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_response_at_type_0 = isoparse(data)

                return first_response_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        first_response_at = _parse_first_response_at(d.pop("first_response_at", UNSET))

        def _parse_last_message_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_message_at_type_0 = isoparse(data)

                return last_message_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_message_at = _parse_last_message_at(d.pop("last_message_at", UNSET))

        participants = []
        _participants = d.pop("participants", UNSET)
        for participants_item_data in _participants or []:
            participants_item = ParticipantResponse.from_dict(participants_item_data)

            participants.append(participants_item)

        chat_with_participants = cls(
            uuid=uuid,
            integration_uuid=integration_uuid,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            title=title,
            description=description,
            first_response_at=first_response_at,
            last_message_at=last_message_at,
            participants=participants,
        )

        chat_with_participants.additional_properties = d
        return chat_with_participants

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
