from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.participant_response import ParticipantResponse
from ...types import UNSET, Response


def _get_kwargs(
    chat_uuid: UUID,
    *,
    from_user_uuid: UUID,
    to_user_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_user_uuid = str(from_user_uuid)
    params["from_user_uuid"] = json_from_user_uuid

    json_to_user_uuid = str(to_user_uuid)
    params["to_user_uuid"] = json_to_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/chat/participant/chat/{chat_uuid}/transfer",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, ParticipantResponse]]:
    if response.status_code == 200:
        response_200 = ParticipantResponse.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, ParticipantResponse]]:
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
    from_user_uuid: UUID,
    to_user_uuid: UUID,
) -> Response[Union[Any, HTTPValidationError, ParticipantResponse]]:
    """Transfer chat

     Transfer chat from one manager to another

    Args:
        chat_uuid (UUID):
        from_user_uuid (UUID): Current manager UUID
        to_user_uuid (UUID): New manager UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, ParticipantResponse]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        from_user_uuid=from_user_uuid,
        to_user_uuid=to_user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    from_user_uuid: UUID,
    to_user_uuid: UUID,
) -> Optional[Union[Any, HTTPValidationError, ParticipantResponse]]:
    """Transfer chat

     Transfer chat from one manager to another

    Args:
        chat_uuid (UUID):
        from_user_uuid (UUID): Current manager UUID
        to_user_uuid (UUID): New manager UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, ParticipantResponse]
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        from_user_uuid=from_user_uuid,
        to_user_uuid=to_user_uuid,
    ).parsed


async def asyncio_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    from_user_uuid: UUID,
    to_user_uuid: UUID,
) -> Response[Union[Any, HTTPValidationError, ParticipantResponse]]:
    """Transfer chat

     Transfer chat from one manager to another

    Args:
        chat_uuid (UUID):
        from_user_uuid (UUID): Current manager UUID
        to_user_uuid (UUID): New manager UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, ParticipantResponse]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        from_user_uuid=from_user_uuid,
        to_user_uuid=to_user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    from_user_uuid: UUID,
    to_user_uuid: UUID,
) -> Optional[Union[Any, HTTPValidationError, ParticipantResponse]]:
    """Transfer chat

     Transfer chat from one manager to another

    Args:
        chat_uuid (UUID):
        from_user_uuid (UUID): Current manager UUID
        to_user_uuid (UUID): New manager UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, ParticipantResponse]
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            from_user_uuid=from_user_uuid,
            to_user_uuid=to_user_uuid,
        )
    ).parsed
