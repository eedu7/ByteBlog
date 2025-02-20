import pytest


@pytest.mark.asyncio
async def test_register(client):
    json = {
        "email": "test1223@example.com",
        "password": "Password@123",
        "username": "test1223",
    }
    response = await client.post("/auth/register", json=json)
    assert response.status_code == 200
    assert response.json()["user"]["username"] == json["username"]
