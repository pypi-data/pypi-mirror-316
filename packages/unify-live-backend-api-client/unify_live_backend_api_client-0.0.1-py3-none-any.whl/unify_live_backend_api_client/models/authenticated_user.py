from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthenticatedUser")


@_attrs_define
class AuthenticatedUser:
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
        email (str): Email address
        email_verified (bool): Email verification status
        name (str): Full name
        given_name (str): Given name
        preferred_username (str): Preferred username
        nickname (str): Nickname
        groups (list[str]): User groups
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
    email: str
    email_verified: bool
    name: str
    given_name: str
    preferred_username: str
    nickname: str
    groups: list[str]
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

        email = self.email

        email_verified = self.email_verified

        name = self.name

        given_name = self.given_name

        preferred_username = self.preferred_username

        nickname = self.nickname

        groups = self.groups

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
                "email": email,
                "email_verified": email_verified,
                "name": name,
                "given_name": given_name,
                "preferred_username": preferred_username,
                "nickname": nickname,
                "groups": groups,
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

        email = d.pop("email")

        email_verified = d.pop("email_verified")

        name = d.pop("name")

        given_name = d.pop("given_name")

        preferred_username = d.pop("preferred_username")

        nickname = d.pop("nickname")

        groups = cast(list[str], d.pop("groups"))

        authenticated_user = cls(
            sub=sub,
            iss=iss,
            aud=aud,
            exp=exp,
            iat=iat,
            uid=uid,
            azp=azp,
            auth_time=auth_time,
            acr=acr,
            email=email,
            email_verified=email_verified,
            name=name,
            given_name=given_name,
            preferred_username=preferred_username,
            nickname=nickname,
            groups=groups,
        )

        authenticated_user.additional_properties = d
        return authenticated_user

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
