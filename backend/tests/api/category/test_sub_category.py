from http import HTTPStatus
from typing import Dict
from uuid import uuid4

import pytest
from httpx import AsyncClient

SUB_CATEGORY_API_ENDPOINT: str = "/sub-category"


@pytest.mark.asyncio
async def test_create_sub_category(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["sub_category"]["name"] == mock_sub_category_data["name"]
    assert (
        response.json()["sub_category"]["category_uuid"]
        == mock_sub_category_data["category_uuid"]
    )


@pytest.mark.asyncio
async def test_create_sub_category_no_parent_category_in_db(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    data = mock_sub_category_data.copy()
    data["category_uuid"] = str(uuid4())

    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/", json=data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_create_sub_category_without_json_body(
    client: AsyncClient, auth_headers: Dict[str, str]
):
    response = await client.post(f"{SUB_CATEGORY_API_ENDPOINT}/", headers=auth_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_sub_category_without_auth(
    client: AsyncClient, mock_sub_category_data: Dict[str, str]
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/", json=mock_sub_category_data
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_create_sub_category_re_adding(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["message"]
