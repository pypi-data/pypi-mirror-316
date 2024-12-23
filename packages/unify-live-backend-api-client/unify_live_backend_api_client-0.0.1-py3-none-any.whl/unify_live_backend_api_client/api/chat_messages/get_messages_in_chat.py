from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_response import MessageResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chat_uuid: UUID,
    *,
    limit: Union[Unset, int] = 50,
    before_message_uuid: Union[None, UUID, Unset] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    json_before_message_uuid: Union[None, Unset, str]
    if isinstance(before_message_uuid, Unset):
        json_before_message_uuid = UNSET
    elif isinstance(before_message_uuid, UUID):
        json_before_message_uuid = str(before_message_uuid)
    else:
        json_before_message_uuid = before_message_uuid
    params["before_message_uuid"] = json_before_message_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/messages/chat/{chat_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MessageResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    before_message_uuid: Union[None, UUID, Unset] = UNSET,
) -> Response[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    """Get chat messages

     Retrieve a list of messages from a chat with optional pagination

    Args:
        chat_uuid (UUID):
        limit (Union[Unset, int]): Number of messages to return Default: 50.
        before_message_uuid (Union[None, UUID, Unset]): Get messages before this message UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['MessageResponse']]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        limit=limit,
        before_message_uuid=before_message_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    before_message_uuid: Union[None, UUID, Unset] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    """Get chat messages

     Retrieve a list of messages from a chat with optional pagination

    Args:
        chat_uuid (UUID):
        limit (Union[Unset, int]): Number of messages to return Default: 50.
        before_message_uuid (Union[None, UUID, Unset]): Get messages before this message UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['MessageResponse']]
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        limit=limit,
        before_message_uuid=before_message_uuid,
    ).parsed


async def asyncio_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    before_message_uuid: Union[None, UUID, Unset] = UNSET,
) -> Response[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    """Get chat messages

     Retrieve a list of messages from a chat with optional pagination

    Args:
        chat_uuid (UUID):
        limit (Union[Unset, int]): Number of messages to return Default: 50.
        before_message_uuid (Union[None, UUID, Unset]): Get messages before this message UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['MessageResponse']]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        limit=limit,
        before_message_uuid=before_message_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    before_message_uuid: Union[None, UUID, Unset] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, list["MessageResponse"]]]:
    """Get chat messages

     Retrieve a list of messages from a chat with optional pagination

    Args:
        chat_uuid (UUID):
        limit (Union[Unset, int]): Number of messages to return Default: 50.
        before_message_uuid (Union[None, UUID, Unset]): Get messages before this message UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['MessageResponse']]
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            limit=limit,
            before_message_uuid=before_message_uuid,
        )
    ).parsed
