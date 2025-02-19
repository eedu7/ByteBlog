from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserCRUD
from app.database import get_async_session


def get_user_crud(session: AsyncSession = Depends(get_async_session)) -> UserCRUD:
    return UserCRUD(session=session)
