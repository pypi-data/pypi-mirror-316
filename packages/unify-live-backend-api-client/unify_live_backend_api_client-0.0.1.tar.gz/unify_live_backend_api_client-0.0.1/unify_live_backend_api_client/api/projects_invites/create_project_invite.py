from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_invite_create import ProjectInviteCreate
from ...models.project_invite_response import ProjectInviteResponse
from ...types import Response


def _get_kwargs(
    project_uuid: UUID,
    *,
    body: ProjectInviteCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_uuid}/invites",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ProjectInviteResponse]]:
    if response.status_code == 201:
        response_201 = ProjectInviteResponse.from_dict(response.json())

        return response_201
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ProjectInviteResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectInviteCreate,
) -> Response[Union[HTTPValidationError, ProjectInviteResponse]]:
    """Create project invite

    Args:
        project_uuid (UUID):
        body (ProjectInviteCreate): Schema for creating a new project invite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectInviteResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectInviteCreate,
) -> Optional[Union[HTTPValidationError, ProjectInviteResponse]]:
    """Create project invite

    Args:
        project_uuid (UUID):
        body (ProjectInviteCreate): Schema for creating a new project invite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectInviteResponse]
    """

    return sync_detailed(
        project_uuid=project_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectInviteCreate,
) -> Response[Union[HTTPValidationError, ProjectInviteResponse]]:
    """Create project invite

    Args:
        project_uuid (UUID):
        body (ProjectInviteCreate): Schema for creating a new project invite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectInviteResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectInviteCreate,
) -> Optional[Union[HTTPValidationError, ProjectInviteResponse]]:
    """Create project invite

    Args:
        project_uuid (UUID):
        body (ProjectInviteCreate): Schema for creating a new project invite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectInviteResponse]
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            client=client,
            body=body,
        )
    ).parsed
