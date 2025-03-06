from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import PostCategory


class PostCategoryCRUD(BaseCRUD[PostCategory]):
    """
    CRUD operations for managing post categories in the database.
    Provides methods for retrieving, creating, updating, and deleting post categories.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the PostCategoryCRUD clas with the provided async session.

        Args:
            session (AsyncSession): The SQLAlachemy asynchronous session to interact with the database.
        """
        super().__init__(model=PostCategory, session=session)

    async def get_all_post_categories(
        self, skip: int = 0, limit: int = 100
    ) -> List[PostCategory]:
        """
        Retrieves all post categories with pagination.

        Args:
            skip (int, optional): The number of records to skip. Defaults to 0.
            limit (int, optional): The number of records to retrieve. Defaults to 100.

        Returns:
            List[PostCategory]: A list of post category objects.

        Raises:
            BadRequesetException: If there is an error retrieving post categories.
        """
        try:
            return await self.get_by(skip=skip, limit=limit)
        except Exception as e:
            raise BadRequestException(f"Error on retrieving post categories: {e}")

    async def get_all_post_categories_by_post_uuid(
        self, post_uuid: str, skip: int = 0, limit: int = 100
    ) -> List[PostCategory]:
        """
        Retrieves all post categories associated with a specific post UUID.

        Args:
            post_uuid (str): The UUID of the post.
            skip (int, optional): The number of records to skip. Default to 0.
            limit (int, optional): The number of records to retrieve. Defaults to 100.

        Returns:
            List[PostCategory]: A list of post category objects associated with the post.

        Raises:
            DatabaseException: If there is an error retrieving post categories.
        """
        try:
            filter_ = {"post_uuid": post_uuid}
            return await self.get_by(filters=filter_, skip=skip, limit=limit)
        except Exception as e:
            raise BadRequestException(
                f"Error retrieving post categories by the post UUID: {e}"
            )

    async def get_post_category_by_uuid(self, uuid: UUID) -> PostCategory:
        """
        Retrieves a single post category by its UUID.

        Args:
            uuid (UUID): The UUID of the post category.

        Returns:
            PostCategory: The post category object.

        Raises:
            NotFoundException: If the post category is not found.
            BadRequestException: If there is an error retrieving the post category.
        """
        try:
            post_category = await self.get_by_uuid(uuid)
            if not post_category:
                raise NotFoundException("Post category not found.")
            return post_category
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(f"Error retrieving post category: {e}")

    async def create_post_category(self, data: Dict[str, Any]) -> PostCategory:
        """
        Creates a new post category and associates it with the user who created it.

        Args:
            data (Dict[str, Any]): The data for the new post category.

        Returns:
            PostCategory: The newly created post category object.

        Raises:
            BadRequestException: If there is an error creating the post category.
        """
        try:
            return await self.create(data)
        except Exception as e:
            raise BadRequestException(f"Error creating post category: {e}")

    async def update_post_category(
        self, data: Dict[str, any], post_category_uuid: UUID
    ) -> bool:
        """
        Updates an existing post category.

        Args:
            data (Dict[str, Any]): The updated data for the post category.
            post_category_uuid (UUID): The UUID of the post category to be updated.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            NotFoundException: If the post category is not found.
            BadRequestException: If there is an error updating the post category.
        """
        try:
            post_category = await self.get_post_category_by_uuid(post_category_uuid)
            await self.update(post_category, data)
        except NotFoundException:
            raise
        except Exception as e:
            BadRequestException(f"Error updating post category: {e}")

    async def delete_post_category(self, post_category_uuid: UUID) -> bool:
        """
        Deletes a post category from the database.

        Args:
            post_category_uuid (UUID): The UUID of the post category to be deleted.

        Returns:
            bool: True if deletion was successful, False otherwise.

        Raises:
            NotFoundException: If the post category is not found.
            BadRequestException: If there is an error deleting the post category.
        """
        try:
            post_category = await self.get_post_category_by_uuid(post_category_uuid)
            await self.delete(post_category)
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(f"Error deleting post category: {e}")
