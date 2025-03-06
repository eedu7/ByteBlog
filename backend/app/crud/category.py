from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import Category


class CategoryCRUD(BaseCRUD[Category]):
    """
    Category-specific CRUD operations in the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the CategoryCRUD class with the provided async session and Category Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=Category, session=session)

    async def get_all_categories(
        self, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        """
        Retrieves all categories from the database with pagination support.

        Args:
            skip (int, optional): Number of records to skip. Default to 0.
            limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

        Returns:
            List[Category]: A list of category objects.

        Raises:
            BadRequestException: If an error occurs while retrieving categories.
        """
        try:
            return await self.get_by(skip=skip, limit=limit)
        except Exception as e:
            raise BadRequestException(f"Failed to fetch categories: {e}")

    async def get_category_by_uuid(self, uuid: UUID) -> Category:
        """
        Retrieves a single category by its UUID.

        Args:
            uuid (UUID): The UUID of the category to retrieve.

        Returns:
            Category: The category object if found.

        Raises:
            NotFoundException: If no category is found with the given UUID.
            BadRequestException: If an error occurs during retrieval.
        """
        try:
            category = await self.get_by_uuid(uuid)
            if not category:
                raise NotFoundException(f"Category with UUID '{uuid}' not found")
            return category
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(
                f"Error retrieving category with UUID {uuid}: {e}"
            )

    async def create_category(self, *, name: str, user_uuid: UUID) -> Category:
        """
        Creates a new category in the database.

        Args:
            name (str): The name of the category.
            user_uuid (UUID): The UUID of the user creating the category.

        Returns:
            Category: The newly created category object.

        Raises:
            BadRequestException: If an error occurs while creating the category.
        """
        data = {"created_by": user_uuid, "name": name}
        try:
            category = await self.create(attributes=data)
            return category
        except Exception as e:
            raise BadRequestException(f"Exception on creating the category. {e}")

    async def update_category(
        self, *, category_uuid: UUID, user_uuid: UUID, updated_name: str
    ) -> bool:
        """
        Updates the name of an existing category.

        Args:
            category_uuid (UUID): The UUID of the category to update.
            user_uuid (UUID): The UUID of the user making the update.
            updated_name (str): The new name for the category.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            NotFoundException: If the category is not found.
            BadRequestException: If an error occurs while updating the category.
        """
        data = {"updated_by": user_uuid, "name": updated_name}
        category = await self.get_category_by_uuid(category_uuid)
        try:
            updated = await self.update(category, data)
            if updated:
                return True
            return False
        except Exception as e:
            raise BadRequestException(f"Exception on updating category. {e}")

    async def delete_category(self, category_uuid) -> bool:
        """
        Deletes a category from the database.

        Note: This function currently performs a hard delete, but it can be modified for soft deletion in the future.

        Args:
            category_uuid (UUID): The UUID of the category to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.

        Raises:
            NotFoundException: If the category is not found.
            BadRequestException: If an error occurs while deleting the category.
        """
        # TODO: Make it soft delete
        category = await self.get_category_by_uuid(category_uuid)
        try:
            deleted = await self.delete(category)
            if deleted:
                return True
            return False
        except Exception as e:
            raise BadRequestException(f"Exception on deleting category. {e}")
