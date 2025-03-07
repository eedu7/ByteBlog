from http import HTTPStatus
from typing import Any, Dict
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.schemas.post import PostStatus
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
    assert response.status_code == HTTPStatus.CREATED
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

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_without_auth(
    client: AsyncClient, mock_post_data: Dict[str, Any]
):
    response = await client.post(f"{API_ENDPOINT}/", json=mock_post_data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
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

    assert response.status_code == HTTPStatus.OK
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

    assert response.status_code == HTTPStatus.OK
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

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=mock_post_update_data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == HTTPStatus.NO_CONTENT
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
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    update_data = mock_post_update_data.copy()
    del update_data["title"]
    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=update_data, headers=headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    update_data = mock_post_update_data.copy()
    del update_data["body"]
    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=update_data, headers=headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    data = mock_post_update_data.copy()

    del data["status"]

    response = await client.put(
        f"{API_ENDPOINT}/{post_uuid}", json=data, headers=headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
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

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_partial_update_post(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.patch(
        f"{API_ENDPOINT}/{post_uuid}", json=mock_post_update_data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert updated_post_data["title"] == mock_post_update_data["title"]
    assert updated_post_data["body"] == mock_post_update_data["body"]
    assert updated_post_data["status"] == mock_post_update_data["status"]


@pytest.mark.asyncio
async def test_partial_update_post_title(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
    mock_post_update_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    data = {"title": "Updated title"}
    response = await client.patch(
        f"{API_ENDPOINT}/{post_uuid}", json=data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert updated_post_data["title"] == data["title"]


@pytest.mark.asyncio
async def test_partial_update_post_body(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    data = {"body": "Updated bodyd"}
    response = await client.patch(
        f"{API_ENDPOINT}/{post_uuid}", json=data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert updated_post_data["body"] == data["body"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        ({"status": PostStatus.ARCHIVED}),
        ({"status": PostStatus.DELETED}),
        ({"status": PostStatus.DRAFT}),
        ({"status": PostStatus.PUBLISHED}),
    ],
)
async def test_partial_update_post_status(
    client: AsyncClient, mock_post_data: Dict[str, Any], data: Dict[str, Any]
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/", json=mock_post_data, headers=headers
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.patch(
        f"{API_ENDPOINT}/{post_uuid}", json=data, headers=headers
    )

    updated_post = await client.get(f"{API_ENDPOINT}/{post_uuid}")

    updated_post_data = updated_post.json()

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert updated_post_data["status"] == data["status"]


@pytest.mark.asyncio
async def test_partial_update_post_without_auth(
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

    response = await client.patch(
        f"{API_ENDPOINT}/{post_uuid}", json=mock_post_update_data
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_post(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.delete(f"{API_ENDPOINT}/{post_uuid}", headers=headers)

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_post_no_uuid(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    response = await client.delete(f"{API_ENDPOINT}/", headers=headers)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_delete_post_without_auth(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.delete(
        f"{API_ENDPOINT}/{post_uuid}",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"]


@pytest.mark.asyncio
async def test_delete_post_invalid_uuid(
    client: AsyncClient,
    mock_post_data: Dict[str, Any],
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    created_post = await client.post(
        f"{API_ENDPOINT}/",
        json=mock_post_data,
        headers=headers,
    )
    post_uuid = created_post.json()["post"]["uuid"]

    response = await client.delete(
        f"{API_ENDPOINT}/{post_uuid}-invalid", headers=headers
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_post_no_post(
    client: AsyncClient,
):
    user_data = create_fake_user()

    response = await client.post("/auth/register", json=user_data)

    access_token = response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    no_record_in_db_post_uuid = uuid4()

    response = await client.delete(
        f"{API_ENDPOINT}/{no_record_in_db_post_uuid}", headers=headers
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["message"]
