from typing import Any, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.database import get_async_session
from app.server import create_app


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    app = create_app()
    yield app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db_session) -> AsyncClient:
    async def _get_session():
        return db_session

    app.dependency_overrides[get_async_session] = _get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
