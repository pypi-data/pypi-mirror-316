from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_create import ProjectCreate
from ...models.project_response import ProjectResponse
from ...types import Response


def _get_kwargs(
    project_uuid: UUID,
    *,
    body: ProjectCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_uuid}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, ProjectResponse]]:
    if response.status_code == 200:
        response_200 = ProjectResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, ProjectResponse]]:
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
    body: ProjectCreate,
) -> Response[Union[Any, HTTPValidationError, ProjectResponse]]:
    """Update project details

    Args:
        project_uuid (UUID):
        body (ProjectCreate): Schema for creating a new project. Example: {'description': 'This
            project is for managing customer interactions', 'name': 'My Awesome Project'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, ProjectResponse]]
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
    body: ProjectCreate,
) -> Optional[Union[Any, HTTPValidationError, ProjectResponse]]:
    """Update project details

    Args:
        project_uuid (UUID):
        body (ProjectCreate): Schema for creating a new project. Example: {'description': 'This
            project is for managing customer interactions', 'name': 'My Awesome Project'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, ProjectResponse]
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
    body: ProjectCreate,
) -> Response[Union[Any, HTTPValidationError, ProjectResponse]]:
    """Update project details

    Args:
        project_uuid (UUID):
        body (ProjectCreate): Schema for creating a new project. Example: {'description': 'This
            project is for managing customer interactions', 'name': 'My Awesome Project'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, ProjectResponse]]
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
    body: ProjectCreate,
) -> Optional[Union[Any, HTTPValidationError, ProjectResponse]]:
    """Update project details

    Args:
        project_uuid (UUID):
        body (ProjectCreate): Schema for creating a new project. Example: {'description': 'This
            project is for managing customer interactions', 'name': 'My Awesome Project'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, ProjectResponse]
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            client=client,
            body=body,
        )
    ).parsed
