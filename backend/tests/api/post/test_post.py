from typing import Any, Dict

import pytest
from httpx import AsyncClient
from icecream import ic

from tests.utils.users import create_fake_user

API_ENDPOINT = "/post"


@pytest.fixture
def mock_post_data() -> Dict[str, Any]:
    return {
        "title": "My First Blog Post",
        "body": "This post introduces the topic.",
        "status": "draft",
    }


@pytest.fixture
def mock_post_update_data() -> Dict[str, Any]:
    return {
        "title": "My First Blog Post (Revised)",
        "body": "This post introduces the topic. (Revised)",
        "status": "archived",
    }


@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, mock_post_data: Dict[str, Any]):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    response = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    assert response.json()["message"]
    assert response.json()["post"]


@pytest.mark.asyncio
async def test_create_post_without_title(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]

    data = mock_post_data.copy()
    del data["title"]

    response = await client.post(
        f"{API_ENDPOINT}/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_without_body(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]

    data = mock_post_data.copy()
    del data["body"]

    response = await client.post(
        f"{API_ENDPOINT}/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_without_status(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]

    data = mock_post_data.copy()
    del data["status"]

    response = await client.post(
        f"{API_ENDPOINT}/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_without_auth(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    response = await client.post(f"{API_ENDPOINT}/", json=mock_post_data)
    assert response.status_code == 401
    assert response.json()["message"] == "Authentication required"


@pytest.mark.asyncio
async def test_get_posts(client: AsyncClient, mock_post_data: Dict[str, Any]):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response = await client.get(f"{API_ENDPOINT}/")

    assert response.status_code == 200
    assert response.json()[0]["Post"]["title"] == mock_post_data["title"]
    assert response.json()[0]["Post"]["body"] == mock_post_data["body"]
    assert response.json()[0]["Post"]["status"] == mock_post_data["status"]


@pytest.mark.asyncio
async def test_get_post(client: AsyncClient, mock_post_data: Dict[str, Any]):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = await client.get(f"{API_ENDPOINT}/{created_post.json()['post']['uuid']}")

    assert response.status_code == 200
    assert created_post.json()["post"]["title"] == response.json()["title"]
    assert created_post.json()["post"]["body"] == response.json()["body"]
    assert created_post.json()["post"]["uuid"] == response.json()["uuid"]


@pytest.mark.asyncio
async def test_get_post_invalid_uuid(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = await client.get(
        f"{API_ENDPOINT}/{created_post.json()['post']['uuid']}invalid"
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_post(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    post_uuid = created_post.json()["post"]["uuid"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=mock_post_update_data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == 204
    assert updated_post_data["title"] == mock_post_update_data["title"]
    assert updated_post_data["body"] == mock_post_update_data["body"]
    assert updated_post_data["status"] == mock_post_update_data["status"]


@pytest.mark.asyncio
async def test_update_post_without_title(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    post_uuid = created_post.json()["post"]["uuid"]
    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = mock_post_update_data.copy()
    del update_data["title"]
    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=update_data, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_post_without_body(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    post_uuid = created_post.json()["post"]["uuid"]
    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = mock_post_update_data.copy()
    del update_data["body"]
    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=update_data, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_post_without_status(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    post_uuid = created_post.json()["post"]["uuid"]
    headers = {"Authorization": f"Bearer {access_token}"}

    data = mock_post_update_data.copy()

    del data["status"]

    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=data, headers=headers
    )

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_update_post_without_auth(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    post_uuid = created_post.json()["post"]["uuid"]

    data = mock_post_update_data.copy()

    del data["status"]

    response = await client.put(f"{API_ENDPOINT}/{post_uuid}", json=data)

    assert response.status_code == 401
    assert response.json()["message"]


# @pytest.mark.asyncio
# async def partial_update_post(): ...


# @pytest.mark.asyncio
# async def delete_post(): ...
