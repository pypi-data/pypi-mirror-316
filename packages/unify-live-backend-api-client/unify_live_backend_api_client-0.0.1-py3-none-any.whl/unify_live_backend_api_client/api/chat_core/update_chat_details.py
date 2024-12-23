from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_response import ChatResponse
from ...models.chat_update import ChatUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    chat_uuid: UUID,
    *,
    body: ChatUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/chat/core/{chat_uuid}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ChatResponse.from_dict(response.json())

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
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
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
    body: ChatUpdate,
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
    """Update chat

     Update chat title or status

    Args:
        chat_uuid (UUID):
        body (ChatUpdate): Schema for updating chat settings. Example: {'description': 'Updated
            chat description', 'status': 'closed', 'title': 'Updated Chat Title'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChatResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ChatUpdate,
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    """Update chat

     Update chat title or status

    Args:
        chat_uuid (UUID):
        body (ChatUpdate): Schema for updating chat settings. Example: {'description': 'Updated
            chat description', 'status': 'closed', 'title': 'Updated Chat Title'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChatResponse, HTTPValidationError]
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ChatUpdate,
) -> Response[Union[Any, ChatResponse, HTTPValidationError]]:
    """Update chat

     Update chat title or status

    Args:
        chat_uuid (UUID):
        body (ChatUpdate): Schema for updating chat settings. Example: {'description': 'Updated
            chat description', 'status': 'closed', 'title': 'Updated Chat Title'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChatResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ChatUpdate,
) -> Optional[Union[Any, ChatResponse, HTTPValidationError]]:
    """Update chat

     Update chat title or status

    Args:
        chat_uuid (UUID):
        body (ChatUpdate): Schema for updating chat settings. Example: {'description': 'Updated
            chat description', 'status': 'closed', 'title': 'Updated Chat Title'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChatResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            body=body,
        )
    ).parsed
