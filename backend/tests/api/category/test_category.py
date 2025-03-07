import asyncio
from http import HTTPStatus
from typing import Any, Dict
from uuid import uuid4

import pytest
from httpx import AsyncClient

from tests.utils.users import create_fake_user

API_ENDPOINT: str = "/category"


@pytest.mark.asyncio
async def test_create_category(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    response = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == mock_category_data["name"]


@pytest.mark.asyncio
async def test_create_category_no_json_body(
    client: AsyncClient, auth_headers: Dict[str, str]
):
    response = await client.post(f"{API_ENDPOINT}/", headers=auth_headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_category_no_auth_headers(
    client: AsyncClient, mock_category_data: Dict[str, str]
):
    response = await client.post(f"{API_ENDPOINT}/", json=mock_category_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_create_category_no_auth_no_json(client: AsyncClient):
    response = await client.post(
        f"{API_ENDPOINT}/",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_get_all_categories(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    await client.post(f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers)

    response = await client.get(f"{API_ENDPOINT}/")

    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["name"] == mock_category_data["name"]


@pytest.mark.asyncio
async def test_get_all_categories_no_categories(client: AsyncClient):
    response = await client.get(f"{API_ENDPOINT}/")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_get_category_by_uuid(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]
    response = await client.get(f"{API_ENDPOINT}/{category_uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["uuid"] == category_uuid
    assert response.json()["name"] == mock_category_data["name"]


@pytest.mark.asyncio
async def test_get_category_by_uuid_invalid_uuid(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]
    response = await client.get(f"{API_ENDPOINT}/{category_uuid}-invalid")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_get_category_by_uuid_no_category(client: AsyncClient):
    category_uuid = uuid4()
    response = await client.get(f"{API_ENDPOINT}/{category_uuid}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_update_category(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    mock_update_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.put(
        f"{API_ENDPOINT}/{category_uuid}",
        json=mock_update_category_data,
        headers=auth_headers,
    )

    updated_category = await client.get(f"{API_ENDPOINT}/{category_uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"]
    assert updated_category.json()["uuid"] == category_uuid
    assert updated_category.json()["name"] == mock_update_category_data["name"]


@pytest.mark.asyncio
async def test_update_category_no_auth(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    mock_update_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.put(
        f"{API_ENDPOINT}/{category_uuid}",
        json=mock_update_category_data,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_update_category_no_json(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.put(
        f"{API_ENDPOINT}/{category_uuid}",
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_category_no_category(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    mock_update_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    await client.post(f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers)
    category_uuid = uuid4()

    response = await client.put(
        f"{API_ENDPOINT}/{category_uuid}",
        json=mock_update_category_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_category(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.delete(
        f"{API_ENDPOINT}/{category_uuid}", headers=auth_headers
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_category_no_headers(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.delete(f"{API_ENDPOINT}/{category_uuid}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_category_no_uuid(
    client: AsyncClient,
    auth_headers: Dict[str, str],
):
    response = await client.delete(f"{API_ENDPOINT}/", headers=auth_headers)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_delete_category_incorrect_uuid(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    category = await client.post(
        f"{API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    category_uuid = category.json()["uuid"]

    response = await client.delete(
        f"{API_ENDPOINT}/{category_uuid}-incorrent", headers=auth_headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]
