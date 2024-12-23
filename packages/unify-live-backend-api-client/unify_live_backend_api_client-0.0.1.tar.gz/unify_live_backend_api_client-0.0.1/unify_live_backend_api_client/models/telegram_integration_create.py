from typing import Any, Literal, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TelegramIntegrationCreate")


@_attrs_define
class TelegramIntegrationCreate:
    """
    Attributes:
        name (str): Integration name
        project_uuid (UUID): Project UUID this integration belongs to
        bot_token (str): Telegram bot token from BotFather
        ask_for_phone_number (bool): Ask for phone number
        greetings_message_text (str): Greeting message text
        type_ (Union[Literal['telegram'], Unset]): Must be 'telegram' Default: 'telegram'.
    """

    name: str
    project_uuid: UUID
    bot_token: str
    ask_for_phone_number: bool
    greetings_message_text: str
    type_: Union[Literal["telegram"], Unset] = "telegram"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_uuid = str(self.project_uuid)

        bot_token = self.bot_token

        ask_for_phone_number = self.ask_for_phone_number

        greetings_message_text = self.greetings_message_text

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "project_uuid": project_uuid,
                "bot_token": bot_token,
                "ask_for_phone_number": ask_for_phone_number,
                "greetings_message_text": greetings_message_text,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        project_uuid = UUID(d.pop("project_uuid"))

        bot_token = d.pop("bot_token")

        ask_for_phone_number = d.pop("ask_for_phone_number")

        greetings_message_text = d.pop("greetings_message_text")

        type_ = cast(Union[Literal["telegram"], Unset], d.pop("type", UNSET))
        if type_ != "telegram" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'telegram', got '{type_}'")

        telegram_integration_create = cls(
            name=name,
            project_uuid=project_uuid,
            bot_token=bot_token,
            ask_for_phone_number=ask_for_phone_number,
            greetings_message_text=greetings_message_text,
            type_=type_,
        )

        telegram_integration_create.additional_properties = d
        return telegram_integration_create

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
