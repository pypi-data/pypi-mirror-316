from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_integration_blocked_clients_response_200_item import GetIntegrationBlockedClientsResponse200Item
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    integration_uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/chat/clients/blocked/{integration_uuid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetIntegrationBlockedClientsResponse200Item.from_dict(response_200_item_data)

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
) -> Response[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    integration_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    """Get blocked clients

     Get list of all blocked clients for integration

    Args:
        integration_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['GetIntegrationBlockedClientsResponse200Item']]]
    """

    kwargs = _get_kwargs(
        integration_uuid=integration_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    integration_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    """Get blocked clients

     Get list of all blocked clients for integration

    Args:
        integration_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['GetIntegrationBlockedClientsResponse200Item']]
    """

    return sync_detailed(
        integration_uuid=integration_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    integration_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    """Get blocked clients

     Get list of all blocked clients for integration

    Args:
        integration_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, list['GetIntegrationBlockedClientsResponse200Item']]]
    """

    kwargs = _get_kwargs(
        integration_uuid=integration_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    integration_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, HTTPValidationError, list["GetIntegrationBlockedClientsResponse200Item"]]]:
    """Get blocked clients

     Get list of all blocked clients for integration

    Args:
        integration_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, list['GetIntegrationBlockedClientsResponse200Item']]
    """

    return (
        await asyncio_detailed(
            integration_uuid=integration_uuid,
            client=client,
        )
    ).parsed
