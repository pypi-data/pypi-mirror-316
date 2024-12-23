from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TelegramIntegrationConfig")


@_attrs_define
class TelegramIntegrationConfig:
    """Schema for telegram integration configuration.

    Attributes:
        uuid (Union[None, UUID, Unset]): Config UUID
        integration_uuid (Union[None, UUID, Unset]): Integration UUID
        bot_token (Union[None, Unset, str]): Telegram bot token from BotFather
        bot_username (Union[None, Unset, str]): Telegram bot username
        bot_title (Union[None, Unset, str]): Telegram bot title
        greeting_message_text (Union[None, Unset, str]): Greeting message text
        ask_for_phone_number (Union[None, Unset, bool]): Ask for phone number
    """

    uuid: Union[None, UUID, Unset] = UNSET
    integration_uuid: Union[None, UUID, Unset] = UNSET
    bot_token: Union[None, Unset, str] = UNSET
    bot_username: Union[None, Unset, str] = UNSET
    bot_title: Union[None, Unset, str] = UNSET
    greeting_message_text: Union[None, Unset, str] = UNSET
    ask_for_phone_number: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[None, Unset, str]
        if isinstance(self.uuid, Unset):
            uuid = UNSET
        elif isinstance(self.uuid, UUID):
            uuid = str(self.uuid)
        else:
            uuid = self.uuid

        integration_uuid: Union[None, Unset, str]
        if isinstance(self.integration_uuid, Unset):
            integration_uuid = UNSET
        elif isinstance(self.integration_uuid, UUID):
            integration_uuid = str(self.integration_uuid)
        else:
            integration_uuid = self.integration_uuid

        bot_token: Union[None, Unset, str]
        if isinstance(self.bot_token, Unset):
            bot_token = UNSET
        else:
            bot_token = self.bot_token

        bot_username: Union[None, Unset, str]
        if isinstance(self.bot_username, Unset):
            bot_username = UNSET
        else:
            bot_username = self.bot_username

        bot_title: Union[None, Unset, str]
        if isinstance(self.bot_title, Unset):
            bot_title = UNSET
        else:
            bot_title = self.bot_title

        greeting_message_text: Union[None, Unset, str]
        if isinstance(self.greeting_message_text, Unset):
            greeting_message_text = UNSET
        else:
            greeting_message_text = self.greeting_message_text

        ask_for_phone_number: Union[None, Unset, bool]
        if isinstance(self.ask_for_phone_number, Unset):
            ask_for_phone_number = UNSET
        else:
            ask_for_phone_number = self.ask_for_phone_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if integration_uuid is not UNSET:
            field_dict["integration_uuid"] = integration_uuid
        if bot_token is not UNSET:
            field_dict["bot_token"] = bot_token
        if bot_username is not UNSET:
            field_dict["bot_username"] = bot_username
        if bot_title is not UNSET:
            field_dict["bot_title"] = bot_title
        if greeting_message_text is not UNSET:
            field_dict["greeting_message_text"] = greeting_message_text
        if ask_for_phone_number is not UNSET:
            field_dict["ask_for_phone_number"] = ask_for_phone_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                uuid_type_0 = UUID(data)

                return uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        uuid = _parse_uuid(d.pop("uuid", UNSET))

        def _parse_integration_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                integration_uuid_type_0 = UUID(data)

                return integration_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        integration_uuid = _parse_integration_uuid(d.pop("integration_uuid", UNSET))

        def _parse_bot_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bot_token = _parse_bot_token(d.pop("bot_token", UNSET))

        def _parse_bot_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bot_username = _parse_bot_username(d.pop("bot_username", UNSET))

        def _parse_bot_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bot_title = _parse_bot_title(d.pop("bot_title", UNSET))

        def _parse_greeting_message_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        greeting_message_text = _parse_greeting_message_text(d.pop("greeting_message_text", UNSET))

        def _parse_ask_for_phone_number(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ask_for_phone_number = _parse_ask_for_phone_number(d.pop("ask_for_phone_number", UNSET))

        telegram_integration_config = cls(
            uuid=uuid,
            integration_uuid=integration_uuid,
            bot_token=bot_token,
            bot_username=bot_username,
            bot_title=bot_title,
            greeting_message_text=greeting_message_text,
            ask_for_phone_number=ask_for_phone_number,
        )

        telegram_integration_config.additional_properties = d
        return telegram_integration_config

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
