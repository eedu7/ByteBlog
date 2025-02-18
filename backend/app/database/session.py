from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from app.config import config

engine = create_async_engine(config.POSTGRES_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError as e:
        raise e


Base = declarative_base()
