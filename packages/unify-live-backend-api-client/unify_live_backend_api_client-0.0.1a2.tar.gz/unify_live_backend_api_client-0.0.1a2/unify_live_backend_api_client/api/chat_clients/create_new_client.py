from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.client_create import ClientCreate
from ...models.client_response import ClientResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: ClientCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/chat/clients",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ClientResponse, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ClientResponse.from_dict(response.json())

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
) -> Response[Union[Any, ClientResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClientCreate,
) -> Response[Union[Any, ClientResponse, HTTPValidationError]]:
    """Create new client

     Create a new client for a specific integration

    Args:
        body (ClientCreate): Schema for creating a new client. Example: {'email':
            'john@example.com', 'external_id': 'telegram123456', 'first_name': 'John',
            'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'last_name': 'Doe', 'phone':
            '+1234567890'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClientResponse, HTTPValidationError]]
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
    body: ClientCreate,
) -> Optional[Union[Any, ClientResponse, HTTPValidationError]]:
    """Create new client

     Create a new client for a specific integration

    Args:
        body (ClientCreate): Schema for creating a new client. Example: {'email':
            'john@example.com', 'external_id': 'telegram123456', 'first_name': 'John',
            'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'last_name': 'Doe', 'phone':
            '+1234567890'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClientResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClientCreate,
) -> Response[Union[Any, ClientResponse, HTTPValidationError]]:
    """Create new client

     Create a new client for a specific integration

    Args:
        body (ClientCreate): Schema for creating a new client. Example: {'email':
            'john@example.com', 'external_id': 'telegram123456', 'first_name': 'John',
            'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'last_name': 'Doe', 'phone':
            '+1234567890'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClientResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClientCreate,
) -> Optional[Union[Any, ClientResponse, HTTPValidationError]]:
    """Create new client

     Create a new client for a specific integration

    Args:
        body (ClientCreate): Schema for creating a new client. Example: {'email':
            'john@example.com', 'external_id': 'telegram123456', 'first_name': 'John',
            'integration_uuid': '123e4567-e89b-12d3-a456-426614174000', 'last_name': 'Doe', 'phone':
            '+1234567890'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClientResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
