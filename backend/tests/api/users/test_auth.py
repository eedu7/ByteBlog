import pytest
from httpx import AsyncClient

from tests.utils.users import create_fake_user


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    fake_user = create_fake_user()
    response = await client.post("/auth/register", json=fake_user)
    assert response.status_code == 201
    response_data = response.json()
    assert "token" in response_data
    assert "access_token" in response_data["token"]
    assert "refresh_token" in response_data["token"]
    assert "expires_in" in response_data["token"]
    assert "token_type" in response_data["token"]
    assert "user" in response_data
    assert "email" in response_data["user"]
    assert "uuid" in response_data["user"]
    assert "username" in response_data["user"]


@pytest.mark.asyncio
async def test_register_user_with_existing_email(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    await client.post("/auth/register", json=fake_user)

    response = await client.post("/auth/register", json=fake_user)

    assert response.status_code == 400
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_register_user_with_existing_username(client: AsyncClient) -> None:
    fake_user = create_fake_user()

    await client.post("/auth/register", json=fake_user)

    response = await client.post("/auth/register", json=fake_user)

    assert response.status_code == 400
    assert response.json()["message"] is not None


@pytest.mark.asyncio
async def test_register_user_with_invalid_email(client: AsyncClient) -> None:
    fake_user = create_fake_user()
    fake_user["email"] = "invalid email"

    response = await client.post("/auth/register", json=fake_user)

    assert response.status_code == 422
    assert response.json()["detail"] is not None
