from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_project_user_response import PaginatedResponseProjectUserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_uuid: UUID,
    *,
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    search: Union[None, Unset, str] = UNSET,
    sort_by: Union[None, Unset, str] = UNSET,
    sort_order: Union[None, Unset, str] = "desc",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    json_search: Union[None, Unset, str]
    if isinstance(search, Unset):
        json_search = UNSET
    else:
        json_search = search
    params["search"] = json_search

    json_sort_by: Union[None, Unset, str]
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    else:
        json_sort_by = sort_by
    params["sort_by"] = json_sort_by

    json_sort_order: Union[None, Unset, str]
    if isinstance(sort_order, Unset):
        json_sort_order = UNSET
    else:
        json_sort_order = sort_order
    params["sort_order"] = json_sort_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_uuid}/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseProjectUserResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
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
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    search: Union[None, Unset, str] = UNSET,
    sort_by: Union[None, Unset, str] = UNSET,
    sort_order: Union[None, Unset, str] = "desc",
) -> Response[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
    """Get project users

     Retrieves a paginated list of project users with optional search and filtering.

    Args:
        project_uuid (UUID):
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        search (Union[None, Unset, str]):
        sort_by (Union[None, Unset, str]):
        sort_order (Union[None, Unset, str]):  Default: 'desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        page=page,
        size=size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    search: Union[None, Unset, str] = UNSET,
    sort_by: Union[None, Unset, str] = UNSET,
    sort_order: Union[None, Unset, str] = "desc",
) -> Optional[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
    """Get project users

     Retrieves a paginated list of project users with optional search and filtering.

    Args:
        project_uuid (UUID):
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        search (Union[None, Unset, str]):
        sort_by (Union[None, Unset, str]):
        sort_order (Union[None, Unset, str]):  Default: 'desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseProjectUserResponse]
    """

    return sync_detailed(
        project_uuid=project_uuid,
        client=client,
        page=page,
        size=size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    ).parsed


async def asyncio_detailed(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    search: Union[None, Unset, str] = UNSET,
    sort_by: Union[None, Unset, str] = UNSET,
    sort_order: Union[None, Unset, str] = "desc",
) -> Response[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
    """Get project users

     Retrieves a paginated list of project users with optional search and filtering.

    Args:
        project_uuid (UUID):
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        search (Union[None, Unset, str]):
        sort_by (Union[None, Unset, str]):
        sort_order (Union[None, Unset, str]):  Default: 'desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
        page=page,
        size=size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_uuid: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    size: Union[Unset, int] = 10,
    search: Union[None, Unset, str] = UNSET,
    sort_by: Union[None, Unset, str] = UNSET,
    sort_order: Union[None, Unset, str] = "desc",
) -> Optional[Union[HTTPValidationError, PaginatedResponseProjectUserResponse]]:
    """Get project users

     Retrieves a paginated list of project users with optional search and filtering.

    Args:
        project_uuid (UUID):
        page (Union[Unset, int]):  Default: 1.
        size (Union[Unset, int]):  Default: 10.
        search (Union[None, Unset, str]):
        sort_by (Union[None, Unset, str]):
        sort_order (Union[None, Unset, str]):  Default: 'desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseProjectUserResponse]
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            client=client,
            page=page,
            size=size,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    ).parsed
