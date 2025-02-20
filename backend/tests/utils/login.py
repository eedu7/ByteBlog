from httpx import AsyncClient

from .users import create_fake_user


async def _create_user_and_login(
    client: AsyncClient, fake_user=create_fake_user()
) -> None:
    await client.post("/auth/register", json=fake_user)
    login_data = {"email": fake_user["email"], "password": fake_user["password"]}
    response = await client.post("/auth/login", json=login_data)
    access_token = response.json()["token"]["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return None


__all__ = ["_create_user_and_login"]
