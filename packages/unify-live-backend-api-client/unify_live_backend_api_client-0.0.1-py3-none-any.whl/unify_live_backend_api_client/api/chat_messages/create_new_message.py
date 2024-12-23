from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_create import MessageCreate
from ...models.message_response import MessageResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: MessageCreate,
    participant_uuid: UUID,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_participant_uuid = str(participant_uuid)
    params["participant_uuid"] = json_participant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/chat/messages",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    if response.status_code == 201:
        response_201 = MessageResponse.from_dict(response.json())

        return response_201
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
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MessageCreate,
    participant_uuid: UUID,
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    """Create message

     Create a new message in chat

    Args:
        participant_uuid (UUID): UUID of message sender
        body (MessageCreate): Schema for creating a new message in the system. Example:
            {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help
            you today?', 'message_type': 'text'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        participant_uuid=participant_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: MessageCreate,
    participant_uuid: UUID,
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    """Create message

     Create a new message in chat

    Args:
        participant_uuid (UUID): UUID of message sender
        body (MessageCreate): Schema for creating a new message in the system. Example:
            {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help
            you today?', 'message_type': 'text'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        participant_uuid=participant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MessageCreate,
    participant_uuid: UUID,
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    """Create message

     Create a new message in chat

    Args:
        participant_uuid (UUID): UUID of message sender
        body (MessageCreate): Schema for creating a new message in the system. Example:
            {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help
            you today?', 'message_type': 'text'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        participant_uuid=participant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MessageCreate,
    participant_uuid: UUID,
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    """Create message

     Create a new message in chat

    Args:
        participant_uuid (UUID): UUID of message sender
        body (MessageCreate): Schema for creating a new message in the system. Example:
            {'chat_uuid': '123e4567-e89b-12d3-a456-426614174000', 'content': 'Hello! How can I help
            you today?', 'message_type': 'text'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            participant_uuid=participant_uuid,
        )
    ).parsed
