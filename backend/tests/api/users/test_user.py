from typing import Any, Dict

import pytest
from httpx import AsyncClient

from tests.utils.users import create_fake_user


@pytest.fixture
def mock_update_data():
    return {
        "full_name": "John Doe",
        "bio": "mybio",
    }


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.get(
        "/user/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_current_user_profile(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.get(
        "/user/user-profile", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == fake_user["email"]
    assert response.json()["username"] == fake_user["username"]


@pytest.mark.asyncio
async def test_get_user_by_uuid(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.get(
        f"/user/{register_response.json()['user']['uuid']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == fake_user["email"]
    assert response.json()["username"] == fake_user["username"]


@pytest.mark.asyncio
async def test_update_user_profile(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.put(
        f"/user/{register_response.json()['user']['uuid']}",
        json=mock_update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_update_user_profile_without_bio(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    update_data = mock_update_data.copy()
    del update_data["bio"]

    response = await client.put(
        f"/user/{register_response.json()['user']['uuid']}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_update_user_profile_without_full_name(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    update_data = mock_update_data.copy()
    update_data.pop("full_name")

    response = await client.put(
        f"/user/{register_response.json()['user']['uuid']}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_update_user_profile_without_any_data(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.put(
        f"/user/{register_response.json()['user']['uuid']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_partial_update_user_profile(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    update_data = mock_update_data.copy()

    response = await client.patch(
        f"/user/{register_response.json()['user']['uuid']}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_partial_update_user_profile_without_bio(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    update_data = mock_update_data.copy()
    del update_data["bio"]

    response = await client.patch(
        f"/user/{register_response.json()['user']['uuid']}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_partial_update_user_profile_without_full_name(
    client: AsyncClient, mock_update_data: Dict[str, Any]
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    update_data = mock_update_data.copy()
    del update_data["full_name"]

    response = await client.patch(
        f"/user/{register_response.json()['user']['uuid']}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_partial_update_user_profile_without_any_data(
    client: AsyncClient,
) -> None:
    fake_user = create_fake_user()

    register_response = await client.post("/auth/register", json=fake_user)

    access_token = register_response.json()["token"]["access_token"]

    response = await client.patch(
        f"/user/{register_response.json()['user']['uuid']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
    assert response.json()["detail"] is not None


# TODO: Delete user profile API test
