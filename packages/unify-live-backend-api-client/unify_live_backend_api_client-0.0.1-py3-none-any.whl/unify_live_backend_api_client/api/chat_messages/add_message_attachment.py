from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_attachment import MessageAttachment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    message_uuid: UUID,
    *,
    file_type: str,
    file_url: str,
    file_name: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["file_type"] = file_type

    params["file_url"] = file_url

    json_file_name: Union[None, Unset, str]
    if isinstance(file_name, Unset):
        json_file_name = UNSET
    else:
        json_file_name = file_name
    params["file_name"] = json_file_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/chat/messages/{message_uuid}/attachments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, MessageAttachment]]:
    if response.status_code == 200:
        response_200 = MessageAttachment.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, MessageAttachment]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: str,
    file_url: str,
    file_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError, MessageAttachment]]:
    """Add attachment

     Add file attachment to message

    Args:
        message_uuid (UUID):
        file_type (str): Type of file
        file_url (str): URL to file
        file_name (Union[None, Unset, str]): Original filename

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageAttachment]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
        file_type=file_type,
        file_url=file_url,
        file_name=file_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: str,
    file_url: str,
    file_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, MessageAttachment]]:
    """Add attachment

     Add file attachment to message

    Args:
        message_uuid (UUID):
        file_type (str): Type of file
        file_url (str): URL to file
        file_name (Union[None, Unset, str]): Original filename

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageAttachment]
    """

    return sync_detailed(
        message_uuid=message_uuid,
        client=client,
        file_type=file_type,
        file_url=file_url,
        file_name=file_name,
    ).parsed


async def asyncio_detailed(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: str,
    file_url: str,
    file_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError, MessageAttachment]]:
    """Add attachment

     Add file attachment to message

    Args:
        message_uuid (UUID):
        file_type (str): Type of file
        file_url (str): URL to file
        file_name (Union[None, Unset, str]): Original filename

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageAttachment]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
        file_type=file_type,
        file_url=file_url,
        file_name=file_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
    file_type: str,
    file_url: str,
    file_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, MessageAttachment]]:
    """Add attachment

     Add file attachment to message

    Args:
        message_uuid (UUID):
        file_type (str): Type of file
        file_url (str): URL to file
        file_name (Union[None, Unset, str]): Original filename

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageAttachment]
    """

    return (
        await asyncio_detailed(
            message_uuid=message_uuid,
            client=client,
            file_type=file_type,
            file_url=file_url,
            file_name=file_name,
        )
    ).parsed
