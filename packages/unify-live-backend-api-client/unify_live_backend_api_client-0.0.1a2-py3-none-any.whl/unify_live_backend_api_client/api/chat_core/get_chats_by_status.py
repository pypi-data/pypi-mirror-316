from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_status import ChatStatus
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_chat_response import PaginatedResponseChatResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    status: ChatStatus,
    *,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/core/status/{status}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseChatResponse.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    status: ChatStatus,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    """Get chats by status

     Get all chats with specific status from all accessible integrations

    Args:
        status (ChatStatus): Available chat statuses.
        offset (Union[Unset, int]): Query offset Default: 0.
        limit (Union[Unset, int]): Items per page Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]
    """

    kwargs = _get_kwargs(
        status=status,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    status: ChatStatus,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    """Get chats by status

     Get all chats with specific status from all accessible integrations

    Args:
        status (ChatStatus): Available chat statuses.
        offset (Union[Unset, int]): Query offset Default: 0.
        limit (Union[Unset, int]): Items per page Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PaginatedResponseChatResponse]
    """

    return sync_detailed(
        status=status,
        client=client,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    status: ChatStatus,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    """Get chats by status

     Get all chats with specific status from all accessible integrations

    Args:
        status (ChatStatus): Available chat statuses.
        offset (Union[Unset, int]): Query offset Default: 0.
        limit (Union[Unset, int]): Items per page Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]
    """

    kwargs = _get_kwargs(
        status=status,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    status: ChatStatus,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Any, HTTPValidationError, PaginatedResponseChatResponse]]:
    """Get chats by status

     Get all chats with specific status from all accessible integrations

    Args:
        status (ChatStatus): Available chat statuses.
        offset (Union[Unset, int]): Query offset Default: 0.
        limit (Union[Unset, int]): Items per page Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PaginatedResponseChatResponse]
    """

    return (
        await asyncio_detailed(
            status=status,
            client=client,
            offset=offset,
            limit=limit,
        )
    ).parsed
