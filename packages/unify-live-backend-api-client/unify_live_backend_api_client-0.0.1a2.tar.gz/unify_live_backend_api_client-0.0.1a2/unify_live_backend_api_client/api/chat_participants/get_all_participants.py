from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.participant_response import ParticipantResponse
from ...models.participant_type import ParticipantType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chat_uuid: UUID,
    *,
    participant_type: Union[None, ParticipantType, Unset] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_participant_type: Union[None, Unset, str]
    if isinstance(participant_type, Unset):
        json_participant_type = UNSET
    elif isinstance(participant_type, ParticipantType):
        json_participant_type = participant_type.value
    else:
        json_participant_type = participant_type
    params["participant_type"] = json_participant_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/participant/chat/{chat_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ParticipantResponse.from_dict(response_200_item_data)

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
) -> Response[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
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
    participant_type: Union[None, ParticipantType, Unset] = UNSET,
) -> Response[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
    """Get participant

     Get all participant in chat with optional type filter

    Args:
        chat_uuid (UUID):
        participant_type (Union[None, ParticipantType, Unset]): Filter by participant type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['ParticipantResponse']]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        participant_type=participant_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    participant_type: Union[None, ParticipantType, Unset] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
    """Get participant

     Get all participant in chat with optional type filter

    Args:
        chat_uuid (UUID):
        participant_type (Union[None, ParticipantType, Unset]): Filter by participant type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['ParticipantResponse']]
    """

    return sync_detailed(
        chat_uuid=chat_uuid,
        client=client,
        participant_type=participant_type,
    ).parsed


async def asyncio_detailed(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    participant_type: Union[None, ParticipantType, Unset] = UNSET,
) -> Response[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
    """Get participant

     Get all participant in chat with optional type filter

    Args:
        chat_uuid (UUID):
        participant_type (Union[None, ParticipantType, Unset]): Filter by participant type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['ParticipantResponse']]]
    """

    kwargs = _get_kwargs(
        chat_uuid=chat_uuid,
        participant_type=participant_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chat_uuid: UUID,
    *,
    client: AuthenticatedClient,
    participant_type: Union[None, ParticipantType, Unset] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, list["ParticipantResponse"]]]:
    """Get participant

     Get all participant in chat with optional type filter

    Args:
        chat_uuid (UUID):
        participant_type (Union[None, ParticipantType, Unset]): Filter by participant type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['ParticipantResponse']]
    """

    return (
        await asyncio_detailed(
            chat_uuid=chat_uuid,
            client=client,
            participant_type=participant_type,
        )
    ).parsed
