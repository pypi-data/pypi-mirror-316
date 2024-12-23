from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TokenResponseWithoutRefresh")


@_attrs_define
class TokenResponseWithoutRefresh:
    """
    Attributes:
        access_token (str): The token used to authenticate and authorize API requests. Typically a JWT or opaque string.
        token_type (str): Specifies the type of token issued. Commonly 'Bearer', indicating how the access_token should
            be included in requests.
        expires_in (int): The duration in seconds for which the access token is valid. After expiration, a new token
            must be obtained.
        id_token (str): A JWT that contains identity claims about the authenticated user. Used in OpenID Connect
            scenarios.
    """

    access_token: str
    token_type: str
    expires_in: int
    id_token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        token_type = self.token_type

        expires_in = self.expires_in

        id_token = self.id_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
                "token_type": token_type,
                "expires_in": expires_in,
                "id_token": id_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        token_type = d.pop("token_type")

        expires_in = d.pop("expires_in")

        id_token = d.pop("id_token")

        token_response_without_refresh = cls(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            id_token=id_token,
        )

        token_response_without_refresh.additional_properties = d
        return token_response_without_refresh

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
