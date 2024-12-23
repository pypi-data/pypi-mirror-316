from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_attachment import MessageAttachment
from ...types import Response


def _get_kwargs(
    message_uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/messages/{message_uuid}/attachments",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MessageAttachment.from_dict(response_200_item_data)

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
) -> Response[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
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
) -> Response[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
    """Get attachments

     Get all attachments for message

    Args:
        message_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['MessageAttachment']]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
    """Get attachments

     Get all attachments for message

    Args:
        message_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['MessageAttachment']]
    """

    return sync_detailed(
        message_uuid=message_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
    """Get attachments

     Get all attachments for message

    Args:
        message_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['MessageAttachment']]]
    """

    kwargs = _get_kwargs(
        message_uuid=message_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, list["MessageAttachment"]]]:
    """Get attachments

     Get all attachments for message

    Args:
        message_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['MessageAttachment']]
    """

    return (
        await asyncio_detailed(
            message_uuid=message_uuid,
            client=client,
        )
    ).parsed
