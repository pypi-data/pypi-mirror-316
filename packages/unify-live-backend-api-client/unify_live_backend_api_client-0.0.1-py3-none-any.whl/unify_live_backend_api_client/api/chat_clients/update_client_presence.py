from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.client_presence import ClientPresence
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    client_uuid: UUID,
    *,
    is_online: bool,
    current_chat_uuid: Union[None, UUID, Unset] = UNSET,
    activity: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_online"] = is_online

    json_current_chat_uuid: Union[None, Unset, str]
    if isinstance(current_chat_uuid, Unset):
        json_current_chat_uuid = UNSET
    elif isinstance(current_chat_uuid, UUID):
        json_current_chat_uuid = str(current_chat_uuid)
    else:
        json_current_chat_uuid = current_chat_uuid
    params["current_chat_uuid"] = json_current_chat_uuid

    json_activity: Union[None, Unset, str]
    if isinstance(activity, Unset):
        json_activity = UNSET
    else:
        json_activity = activity
    params["activity"] = json_activity

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/chat/clients/{client_uuid}/presence",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ClientPresence, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ClientPresence.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ClientPresence, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    is_online: bool,
    current_chat_uuid: Union[None, UUID, Unset] = UNSET,
    activity: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, ClientPresence, HTTPValidationError]]:
    """Update presence

     Update client's online status and current activity

    Args:
        client_uuid (UUID):
        is_online (bool): Online status
        current_chat_uuid (Union[None, UUID, Unset]): Current active chat UUID
        activity (Union[None, Unset, str]): Current activity description

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClientPresence, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client_uuid=client_uuid,
        is_online=is_online,
        current_chat_uuid=current_chat_uuid,
        activity=activity,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    is_online: bool,
    current_chat_uuid: Union[None, UUID, Unset] = UNSET,
    activity: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, ClientPresence, HTTPValidationError]]:
    """Update presence

     Update client's online status and current activity

    Args:
        client_uuid (UUID):
        is_online (bool): Online status
        current_chat_uuid (Union[None, UUID, Unset]): Current active chat UUID
        activity (Union[None, Unset, str]): Current activity description

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClientPresence, HTTPValidationError]
    """

    return sync_detailed(
        client_uuid=client_uuid,
        client=client,
        is_online=is_online,
        current_chat_uuid=current_chat_uuid,
        activity=activity,
    ).parsed


async def asyncio_detailed(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    is_online: bool,
    current_chat_uuid: Union[None, UUID, Unset] = UNSET,
    activity: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, ClientPresence, HTTPValidationError]]:
    """Update presence

     Update client's online status and current activity

    Args:
        client_uuid (UUID):
        is_online (bool): Online status
        current_chat_uuid (Union[None, UUID, Unset]): Current active chat UUID
        activity (Union[None, Unset, str]): Current activity description

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClientPresence, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client_uuid=client_uuid,
        is_online=is_online,
        current_chat_uuid=current_chat_uuid,
        activity=activity,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    is_online: bool,
    current_chat_uuid: Union[None, UUID, Unset] = UNSET,
    activity: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, ClientPresence, HTTPValidationError]]:
    """Update presence

     Update client's online status and current activity

    Args:
        client_uuid (UUID):
        is_online (bool): Online status
        current_chat_uuid (Union[None, UUID, Unset]): Current active chat UUID
        activity (Union[None, Unset, str]): Current activity description

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClientPresence, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client_uuid=client_uuid,
            client=client,
            is_online=is_online,
            current_chat_uuid=current_chat_uuid,
            activity=activity,
        )
    ).parsed
