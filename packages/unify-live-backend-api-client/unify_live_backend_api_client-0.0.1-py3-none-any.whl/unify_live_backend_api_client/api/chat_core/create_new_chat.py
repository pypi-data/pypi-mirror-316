from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_create import ChatCreate
from ...models.chat_response import ChatResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: ChatCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/chat/core",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ChatResponse.from_dict(response.json())

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
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ChatCreate,
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
    """Create new chat

     Create a new chat for specific integration

    Args:
        body (ChatCreate): Schema for creating a new chat. Example: {'description': 'General
            support discussion', 'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'title':
            'Support Chat'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChatResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ChatCreate,
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    """Create new chat

     Create a new chat for specific integration

    Args:
        body (ChatCreate): Schema for creating a new chat. Example: {'description': 'General
            support discussion', 'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'title':
            'Support Chat'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChatResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ChatCreate,
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
    """Create new chat

     Create a new chat for specific integration

    Args:
        body (ChatCreate): Schema for creating a new chat. Example: {'description': 'General
            support discussion', 'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'title':
            'Support Chat'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChatResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ChatCreate,
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    """Create new chat

     Create a new chat for specific integration

    Args:
        body (ChatCreate): Schema for creating a new chat. Example: {'description': 'General
            support discussion', 'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'title':
            'Support Chat'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChatResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
