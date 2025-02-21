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


@pytest.mark.asyncio
async def test_user_login(client: AsyncClient):
    fake_user = create_fake_user()

    await client.post("/auth/register", json=fake_user)

    login_data = {"email": fake_user["email"], "password": fake_user["password"]}

    response = await client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    assert response.json()["token"] is not None
    assert response.json()["token"]["access_token"] is not None
    assert response.json()["token"]["refresh_token"] is not None
    assert response.json()["user"] is not None
    assert response.json()["user"]["email"] is not None
    assert response.json()["user"]["username"] is not None
    assert response.json()["user"]["uuid"] is not None


@pytest.mark.asyncio
async def test_user_login_with_invalid_email(client: AsyncClient):
    fake_user = create_fake_user()
    fake_user["email"] = "invalid_email"

    response = await client.post("/auth/login", json=fake_user)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_user_login_with_incorrect_password(client: AsyncClient):
    fake_user = create_fake_user()

    await client.post("/auth/register", json=fake_user)
    login_data = {"email": fake_user["email"], "password": "incorrect password"}

    response = await client.post("auth/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["message"] is not None
