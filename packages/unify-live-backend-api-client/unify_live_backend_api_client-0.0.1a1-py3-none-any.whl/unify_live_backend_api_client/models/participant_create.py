from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.participant_type import ParticipantType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantCreate")


@_attrs_define
class ParticipantCreate:
    """Schema for adding a participant to chat.

    Example:
        {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'client_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'participant_type': 'client'}

    Attributes:
        chat_uuid (UUID): Chat UUID
        participant_type (ParticipantType): Types of chat participant.
        user_uuid (Union[None, UUID, Unset]): User UUID (for managers)
        client_uuid (Union[None, UUID, Unset]): Client UUID (for clients)
    """

    chat_uuid: UUID
    participant_type: ParticipantType
    user_uuid: Union[None, UUID, Unset] = UNSET
    client_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chat_uuid = str(self.chat_uuid)

        participant_type = self.participant_type.value

        user_uuid: Union[None, Unset, str]
        if isinstance(self.user_uuid, Unset):
            user_uuid = UNSET
        elif isinstance(self.user_uuid, UUID):
            user_uuid = str(self.user_uuid)
        else:
            user_uuid = self.user_uuid

        client_uuid: Union[None, Unset, str]
        if isinstance(self.client_uuid, Unset):
            client_uuid = UNSET
        elif isinstance(self.client_uuid, UUID):
            client_uuid = str(self.client_uuid)
        else:
            client_uuid = self.client_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat_uuid": chat_uuid,
                "participant_type": participant_type,
            }
        )
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if client_uuid is not UNSET:
            field_dict["client_uuid"] = client_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        chat_uuid = UUID(d.pop("chat_uuid"))

        participant_type = ParticipantType(d.pop("participant_type"))

        def _parse_user_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_uuid_type_0 = UUID(data)

                return user_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        user_uuid = _parse_user_uuid(d.pop("user_uuid", UNSET))

        def _parse_client_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                client_uuid_type_0 = UUID(data)

                return client_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        client_uuid = _parse_client_uuid(d.pop("client_uuid", UNSET))

        participant_create = cls(
            chat_uuid=chat_uuid,
            participant_type=participant_type,
            user_uuid=user_uuid,
            client_uuid=client_uuid,
        )

        participant_create.additional_properties = d
        return participant_create

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
