import asyncio
from typing import Generator

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import Any
from fastapi import FastAPI
from app.config import config
from app.models import Base
from app.server import create_app

test_engine = create_async_engine(config.TEST_POSTGRES_URL, echo=True)
TESTSessionLocal = async_sessionmaker(
    bind=test_engine, autocommit=False, autoflush=False
)

@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    app = create_app()
    return app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield TESTSessionLocal()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app, base_url="http://test") as ac:
        yield ac
