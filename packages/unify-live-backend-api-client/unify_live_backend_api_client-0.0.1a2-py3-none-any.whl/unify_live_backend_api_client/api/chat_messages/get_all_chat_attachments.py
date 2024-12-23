from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chat_uuid: UUID,
    *,
    file_type: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_file_type: Union[None, Unset, str]
    if isinstance(file_type, Unset):
        json_file_type = UNSET
    else:
        json_file_type = file_type
    params["file_type"] = json_file_type

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/messages/chat/{chat_uuid}/attachments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
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
    file_type: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get chat attachments

     Get all attachments in chat with pagination

    Args:
        chat_uuid (UUID):
        file_type (Union[None, Unset, str]): Filter by file type
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        file_type=file_type,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get chat attachments

     Get all attachments in chat with pagination

    Args:
        chat_uuid (UUID):
        file_type (Union[None, Unset, str]): Filter by file type
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        file_type=file_type,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get chat attachments

     Get all attachments in chat with pagination

    Args:
        chat_uuid (UUID):
        file_type (Union[None, Unset, str]): Filter by file type
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        file_type=file_type,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get chat attachments

     Get all attachments in chat with pagination

    Args:
        chat_uuid (UUID):
        file_type (Union[None, Unset, str]): Filter by file type
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            file_type=file_type,
            limit=limit,
            offset=offset,
        )
    ).parsed
