from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models import PostCategory


class PostCategoryCRUD(BaseCRUD[PostCategory]):
    """
    PostCategory-specific CRUD in the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the PostCategoryCRUD class with the provided async session and PostCategory Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=PostCategory, session=session)

    async def get_all_post_categories(self, skip: int = 0, limit: int = 100):
        """
        Retrieves all post categories from the database.

        Args:
            skip (int, optional): The number of post categories to skip. Defaults to 0.
            limit (int, optional): The maximum number of post categories to retrieve. Defaults to 100.

        Returns:
            List[PostCategory]: A list of post categories retrieved from the database.
        """
        return await self.get_by(skip=skip, limit=limit)

    async def get_all_post_categories_by_post_uuid(
        self, post_uuid: str, skip: int = 0, limit: int = 100
    ):
        """
        Retrieves all post categories by post uuid from the database.

        Args:
            post_uuid (str): The post uuid to filter post categories.

        Returns:
            List[PostCategory]: A list of post categories retrieved from the database.
        """
        filter_ = {"post_uuid": post_uuid}
        return await self.get_by(filters=filter_, skip=skip, limit=limit)

    async def get_post_category_by_uuid(self, uuid: UUID):
        return await self.get_by_uuid(uuid=uuid)

    async def create_post_category(self, data: Dict[str, Any], user_uuid: UUID):
        data.update({"created_by": user_uuid})
        return await self.create(data)

    async def update_post_category(
        self, data: Dict[str, any], post_category_uuid: UUID, user_uuid: UUID
    ):
        data.update({"updated_by": user_uuid})
        post_category = await self.get_post_category_by_uuid(post_category_uuid)
        await self.update(post_category, data)

    async def delete_post_category(self, post_category_uuid: UUID):
        post_category = await self.get_post_category_by_uuid(post_category_uuid)
        await self.delete(post_category)
