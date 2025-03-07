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


@pytest.mark.asyncio
async def test_get_all_sub_categories(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    response = await client.get(f"{SUB_CATEGORY_API_ENDPOINT}/")

    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["name"] == mock_sub_category_data["name"]
    assert (
        response.json()[0]["category_uuid"] == mock_sub_category_data["category_uuid"]
    )


@pytest.mark.asyncio
async def test_get_sub_category_by_uuid(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = sub_category.json()["sub_category"]
    response = await client.get(f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["sub_category"]["name"] == sub_category["name"]
    assert response.json()["sub_category"]["uuid"] == sub_category["uuid"]
    assert (
        response.json()["sub_category"]["category_uuid"]
        == sub_category["category_uuid"]
    )


@pytest.mark.asyncio
async def test_get_sub_category_by_uuid_invalid_uuid(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = sub_category.json()["sub_category"]
    response = await client.get(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}-invalid"
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_get_sub_category_by_uuid_no_uuid_of_sub_category(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    response = await client.get(f"{SUB_CATEGORY_API_ENDPOINT}/{uuid4()}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_update_sub_category(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
    mock_update_sub_category_data: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = response.json()["sub_category"]

    await client.patch(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}",
        json=mock_update_sub_category_data,
        headers=auth_headers,
    )

    response = await client.get(f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}")

    updated_sub_category = response.json()["sub_category"]

    response = await client.get(f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}")

    assert updated_sub_category["uuid"] == response.json()["sub_category"]["uuid"]
    assert updated_sub_category["name"] == response.json()["sub_category"]["name"]
    assert updated_sub_category["name"] == mock_update_sub_category_data["name"]
    assert (
        updated_sub_category["category_uuid"]
        == response.json()["sub_category"]["category_uuid"]
    )


@pytest.mark.asyncio
async def test_update_sub_category_no_json(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = response.json()["sub_category"]

    response = await client.patch(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}", headers=auth_headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_sub_category_no_auth_headers(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
    mock_update_sub_category_data: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = response.json()["sub_category"]

    response = await client.patch(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}",
        json=mock_update_sub_category_data,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_update_sub_category_invalid_uuid(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
    mock_update_sub_category_data: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = response.json()["sub_category"]

    response = await client.patch(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category['uuid']}-invalid",
        json=mock_update_sub_category_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_sub_category_no_db_saved_uuid(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
    mock_update_sub_category_data: Dict[str, str],
):
    response = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )
    sub_category = response.json()["sub_category"]

    response = await client.patch(
        f"{SUB_CATEGORY_API_ENDPOINT}/{uuid4()}",
        json=mock_update_sub_category_data,
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_sub_category(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    response = await client.delete(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category.json()['sub_category']['uuid']}",
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_sub_category_no_headers(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    response = await client.delete(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category.json()['sub_category']['uuid']}",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_sub_category_invalid_uuid(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    response = await client.delete(
        f"{SUB_CATEGORY_API_ENDPOINT}/{sub_category.json()['sub_category']['uuid']}-invalid",
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_sub_category_with_uuid_no_in_db(
    client: AsyncClient,
    mock_sub_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
):
    sub_category = await client.post(
        f"{SUB_CATEGORY_API_ENDPOINT}/",
        json=mock_sub_category_data,
        headers=auth_headers,
    )

    response = await client.delete(
        f"{SUB_CATEGORY_API_ENDPOINT}/{uuid4()}",
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]
