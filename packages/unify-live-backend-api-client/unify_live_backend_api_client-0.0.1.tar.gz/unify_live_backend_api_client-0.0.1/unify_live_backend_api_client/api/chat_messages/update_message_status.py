from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_response import MessageResponse
from ...models.message_status import MessageStatus
from ...types import Response


def _get_kwargs(
    message_uuid: UUID,
    status: MessageStatus,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/chat/messages/{message_uuid}/status/{status}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    if response.status_code == 200:
        response_200 = MessageResponse.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    message_uuid: UUID,
    status: MessageStatus,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    """Update status

     Update message delivery status

    Args:
        message_uuid (UUID):
        status (MessageStatus): Possible message statuses during delivery lifecycle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageResponse]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_uuid: UUID,
    status: MessageStatus,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    """Update status

     Update message delivery status

    Args:
        message_uuid (UUID):
        status (MessageStatus): Possible message statuses during delivery lifecycle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageResponse]
    """

    return sync_detailed(
        message_uuid=message_uuid,
        status=status,
        client=client,
    ).parsed


async def asyncio_detailed(
    message_uuid: UUID,
    status: MessageStatus,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, MessageResponse]]:
    """Update status

     Update message delivery status

    Args:
        message_uuid (UUID):
        status (MessageStatus): Possible message statuses during delivery lifecycle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageResponse]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_uuid: UUID,
    status: MessageStatus,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, MessageResponse]]:
    """Update status

     Update message delivery status

    Args:
        message_uuid (UUID):
        status (MessageStatus): Possible message statuses during delivery lifecycle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageResponse]
    """

    return (
        await asyncio_detailed(
            message_uuid=message_uuid,
            status=status,
            client=client,
        )
    ).parsed
