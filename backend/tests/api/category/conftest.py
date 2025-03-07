import asyncio
from typing import Any, Dict

import pytest
from httpx import AsyncClient

from tests.utils.users import create_fake_user

CATEGORY_API_ENDPOINT: str = "/category"


@pytest.fixture(scope="function")
def auth_headers(client: AsyncClient) -> Dict[str, str]:
    loop = asyncio.get_event_loop()
    user_data = create_fake_user()
    request = client.post("/auth/register", json=user_data)
    response = loop.run_until_complete(request)
    access_token = response.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def mock_category_data() -> Dict[str, str]:
    return {"name": "Programming"}


@pytest.fixture
def mock_update_category_data() -> Dict[str, str]:
    return {"name": "Web Dev"}


@pytest.fixture(scope="function")
def mock_category(
    client: AsyncClient,
    mock_category_data: Dict[str, str],
    auth_headers: Dict[str, str],
) -> Dict[str, Any]:
    loop = asyncio.get_event_loop()
    request = client.post(
        f"{CATEGORY_API_ENDPOINT}/", json=mock_category_data, headers=auth_headers
    )
    response = loop.run_until_complete(request)
    return response.json()


@pytest.fixture
def mock_sub_category_data(mock_category: Dict[str, str]) -> Dict[str, str]:
    return {"category_uuid": mock_category["uuid"], "name": "Java"}
