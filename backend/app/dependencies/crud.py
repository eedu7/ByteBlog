from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.category import CategoryCRUD
from app.crud.post import PostCRUD
from app.crud.post_category import PostCategoryCRUD
from app.crud.sub_category import SubCategoryCRUD
from app.crud.user import UserCRUD
from app.database import get_async_session


class CRUDProvider:
    @staticmethod
    def get_user_crud(session: AsyncSession = Depends(get_async_session)) -> UserCRUD:
        return UserCRUD(session=session)

    @staticmethod
    def get_post_curd(session: AsyncSession = Depends(get_async_session)) -> PostCRUD:
        return PostCRUD(session=session)

    @staticmethod
    def get_category_crud(
        session: AsyncSession = Depends(get_async_session),
    ) -> CategoryCRUD:
        return CategoryCRUD(session=session)

    @staticmethod
    def get_sub_category_crud(
        session: AsyncSession = Depends(get_async_session),
    ) -> SubCategoryCRUD:
        return SubCategoryCRUD(session=session)

    @staticmethod
    def get_post_category_crud(
        session: AsyncSession = Depends(get_async_session),
    ) -> PostCategoryCRUD:
        return PostCategoryCRUD(session=session)
