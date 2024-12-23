from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageAttachment")


@_attrs_define
class MessageAttachment:
    """Schema for file attachments in messages.

    Example:
        {'file_name': 'vacation-photo.jpg', 'file_type': 'image', 'file_url':
            'https://storage.example.com/files/image.jpg', 'uuid': '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        uuid (UUID): Unique identifier of the attachment
        file_type (str): Type of the attached file (e.g., image, document, video)
        file_url (str): URL where the file can be accessed
        file_name (Union[None, Unset, str]): Original name of the uploaded file
    """

    uuid: UUID
    file_type: str
    file_url: str
    file_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        file_type = self.file_type

        file_url = self.file_url

        file_name: Union[None, Unset, str]
        if isinstance(self.file_name, Unset):
            file_name = UNSET
        else:
            file_name = self.file_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "file_type": file_type,
                "file_url": file_url,
            }
        )
        if file_name is not UNSET:
            field_dict["file_name"] = file_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        file_type = d.pop("file_type")

        file_url = d.pop("file_url")

        def _parse_file_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        message_attachment = cls(
            uuid=uuid,
            file_type=file_type,
            file_url=file_url,
            file_name=file_name,
        )

        message_attachment.additional_properties = d
        return message_attachment

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
