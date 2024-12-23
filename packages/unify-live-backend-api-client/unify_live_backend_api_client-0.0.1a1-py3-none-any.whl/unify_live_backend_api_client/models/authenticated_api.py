from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthenticatedApi")


@_attrs_define
class AuthenticatedApi:
    """
    Attributes:
        sub (str): Subject identifier
        iss (str): Issuer
        aud (str): Audience
        exp (int): Expiration time
        iat (int): Issued at
        uid (str): User ID
        azp (str): Authorized party
        auth_time (int): Authentication time
        acr (str): Authentication context class reference
    """

    sub: str
    iss: str
    aud: str
    exp: int
    iat: int
    uid: str
    azp: str
    auth_time: int
    acr: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sub = self.sub

        iss = self.iss

        aud = self.aud

        exp = self.exp

        iat = self.iat

        uid = self.uid

        azp = self.azp

        auth_time = self.auth_time

        acr = self.acr

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sub": sub,
                "iss": iss,
                "aud": aud,
                "exp": exp,
                "iat": iat,
                "uid": uid,
                "azp": azp,
                "auth_time": auth_time,
                "acr": acr,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        sub = d.pop("sub")

        iss = d.pop("iss")

        aud = d.pop("aud")

        exp = d.pop("exp")

        iat = d.pop("iat")

        uid = d.pop("uid")

        azp = d.pop("azp")

        auth_time = d.pop("auth_time")

        acr = d.pop("acr")

        authenticated_api = cls(
            sub=sub,
            iss=iss,
            aud=aud,
            exp=exp,
            iat=iat,
            uid=uid,
            azp=azp,
            auth_time=auth_time,
            acr=acr,
        )

        authenticated_api.additional_properties = d
        return authenticated_api

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
