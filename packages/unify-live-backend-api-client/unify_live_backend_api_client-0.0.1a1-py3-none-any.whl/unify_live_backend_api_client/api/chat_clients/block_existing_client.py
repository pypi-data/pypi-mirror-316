from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.block_reason import BlockReason
from ...models.block_status import BlockStatus
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    client_uuid: UUID,
    *,
    body: BlockReason,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/chat/clients/{client_uuid}/block",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BlockStatus, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BlockStatus.from_dict(response.json())

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
) -> Response[Union[Any, BlockStatus, HTTPValidationError]]:
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
    body: BlockReason,
) -> Response[Union[Any, BlockStatus, HTTPValidationError]]:
    """Block client

     Block client with reason and optional expiration

    Args:
        client_uuid (UUID):
        body (BlockReason): Schema for client blocking reason. Example: {'blocked_by_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'expires_at': '2024-02-01T00:00:00Z', 'reason':
            'Spam messages'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BlockStatus, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client_uuid=client_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BlockReason,
) -> Optional[Union[Any, BlockStatus, HTTPValidationError]]:
    """Block client

     Block client with reason and optional expiration

    Args:
        client_uuid (UUID):
        body (BlockReason): Schema for client blocking reason. Example: {'blocked_by_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'expires_at': '2024-02-01T00:00:00Z', 'reason':
            'Spam messages'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BlockStatus, HTTPValidationError]
    """

    return sync_detailed(
        client_uuid=client_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BlockReason,
) -> Response[Union[Any, BlockStatus, HTTPValidationError]]:
    """Block client

     Block client with reason and optional expiration

    Args:
        client_uuid (UUID):
        body (BlockReason): Schema for client blocking reason. Example: {'blocked_by_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'expires_at': '2024-02-01T00:00:00Z', 'reason':
            'Spam messages'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BlockStatus, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client_uuid=client_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    client_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BlockReason,
) -> Optional[Union[Any, BlockStatus, HTTPValidationError]]:
    """Block client

     Block client with reason and optional expiration

    Args:
        client_uuid (UUID):
        body (BlockReason): Schema for client blocking reason. Example: {'blocked_by_uuid':
            '123e4567-e89b-12d3-a456-426614174000', 'expires_at': '2024-02-01T00:00:00Z', 'reason':
            'Spam messages'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BlockStatus, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client_uuid=client_uuid,
            client=client,
            body=body,
        )
    ).parsed
