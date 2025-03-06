import asyncio
import os
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.config import config
from app.models import Base

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_egine = create_async_engine(config.TEST_POSTGRES_URL)
    async_session = async_sessionmaker(
        async_egine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        async with async_egine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with async_egine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_egine.dispose()
