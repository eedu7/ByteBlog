from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import PostCRUD
from app.crud.user import UserCRUD
from app.database import get_async_session


def get_user_crud(session: AsyncSession = Depends(get_async_session)) -> UserCRUD:
    return UserCRUD(session=session)


def get_post_curd(session: AsyncSession = Depends(get_async_session)) -> PostCRUD:
    return PostCRUD(session=session)
