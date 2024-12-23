from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_user_response import ProjectUserResponse
from ...types import UNSET, Response


def _get_kwargs(
    project_uuid: UUID,
    user_uuid: UUID,
    *,
    role: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["role"] = role

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_uuid}/users/{user_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ProjectUserResponse]]:
    if response.status_code == 200:
        response_200 = ProjectUserResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ProjectUserResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_uuid: UUID,
    user_uuid: UUID,
    *,
    client: AuthenticatedClient,
    role: str,
) -> Response[Union[HTTPValidationError, ProjectUserResponse]]:
    """Update user role

    Args:
        project_uuid (UUID):
        user_uuid (UUID):
        role (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectUserResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        user_uuid=user_uuid,
        role=role,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_uuid: UUID,
    user_uuid: UUID,
    *,
    client: AuthenticatedClient,
    role: str,
) -> Optional[Union[HTTPValidationError, ProjectUserResponse]]:
    """Update user role

    Args:
        project_uuid (UUID):
        user_uuid (UUID):
        role (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectUserResponse]
    """

    return sync_detailed(
        project_uuid=project_uuid,
        user_uuid=user_uuid,
        client=client,
        role=role,
    ).parsed


async def asyncio_detailed(
    project_uuid: UUID,
    user_uuid: UUID,
    *,
    client: AuthenticatedClient,
    role: str,
) -> Response[Union[HTTPValidationError, ProjectUserResponse]]:
    """Update user role

    Args:
        project_uuid (UUID):
        user_uuid (UUID):
        role (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectUserResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        user_uuid=user_uuid,
        role=role,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_uuid: UUID,
    user_uuid: UUID,
    *,
    client: AuthenticatedClient,
    role: str,
) -> Optional[Union[HTTPValidationError, ProjectUserResponse]]:
    """Update user role

    Args:
        project_uuid (UUID):
        user_uuid (UUID):
        role (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectUserResponse]
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            user_uuid=user_uuid,
            client=client,
            role=role,
        )
    ).parsed
