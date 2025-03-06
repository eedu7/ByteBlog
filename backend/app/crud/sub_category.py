from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import SubCategory


class SubCategoryCRUD(BaseCRUD[SubCategory]):
    """
    SubCategory-specific CRUD operations in the database.

    This class provides method to perform CRUD operations for SubCategory entities.
    Including creating, updating, deleting, and fetching SubCategories by UUID or with pagination.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the PostCRUD class with the provided async session and SubCategory Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=SubCategory, session=session)

    async def get_all_sub_categories(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[SubCategory]:
        """
        Retrieves all sub-categories from the database with pagination support.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

        Returns:
            List[SubCategroy]: A list of SubCategory objects.

        Raises:
            NotFoundException: If no sub-categories are found.
            BadRequestException: If an error occurs while retrieving sub-categories.

        """
        try:
            sub_categories = await self.get_by(skip=skip, limit=limit)
            if not sub_categories:
                raise NotFoundException("No sub-categories found.")
            return sub_categories
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(f"Failed to fetch sub-categories: {e}")

    async def get_sub_category_by_uuid(self, sub_category_uuid: UUID) -> SubCategory:
        """
        Retrieves a single sub-category by its UUID.

        Args:
            sub_category_uuid (UUID): The UUID of the sub-category to retrieve.

        Returns:
            SubCategory: The sub-categroy object if found.

        Raises:
            NotFoundException: If no sub-category is found with the given UUID.
            BadRequestException: If an error occurs while retrieving the sub-category.
        """
        try:
            sub_category = await self.get_by_uuid(sub_category_uuid)

            if not sub_category:
                raise NotFoundException(
                    f"SubCategoet with UUID `{sub_category_uuid}` not found."
                )
            return sub_category
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(
                f"Error retrieving sub-category with UUID `{sub_category_uuid}`: {e}"
            )

    async def create_sub_category(
        self, data: Dict[str, Any], user_uuid: UUID
    ) -> SubCategory:
        """
        Create a new SubCategory in the database.

        Args:
            data (Dict[str, Any]): The data to create the SubCategory.
            user_uuid (UUID): The UUID of the user creating the SubCategory.

        Returns:
            SubCategory: The newly created SubCategory object.

        Raises:
            BadRequestException: If an error occurs while creating the subcategory.
        """
        try:
            data.update({"created_by": user_uuid})
            sub_category = await self.create(data)
            return sub_category
        except Exception as e:
            raise BadRequestException(f"Failed to create sub-category: {e}")

    async def update_sub_category(
        self, data: Dict[str, Any], sub_category_uuid: UUID, user_uuid: UUID
    ) -> bool:
        """
        Updates an existing SubCategory.

        Args:
            data (Dict[str, Any]): The data to update the SubCategory.
            sub_category_uuid (UUID): The UUID of the SubCategory to update.
            user_uuid (UUID): The UUID of the user performing the update.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            NotFoundException: If the SubCategory is not found.
            BadRequestException: If an error occurs while updating the SubCategory.
        """
        try:
            data.update({"updated_by": user_uuid})
            sub_category = await self.get_sub_category_by_uuid(sub_category_uuid)
            return await self.update(sub_category, data)
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(f"Failed to update sub-category: {e}")

    async def delete_sub_category(self, sub_category_uuid: UUID) -> bool:
        """
        Deletes a SubCategory from the database.

        Args:
            sub_category_uuid (UUID): The UUID of the SubCategory to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.

        Raises:
            NotFoundException: If the SubCategory is not found.
            BadRequestException: If an error occurs while deleting the SubCategory.
        """
        try:
            sub_category = await self.get_sub_category_by_uuid(sub_category_uuid)
            return await self.delete(sub_category)
        except NotFoundException:
            raise
        except Exception as e:
            raise BadRequestException(f"Exception on deleting sub-category: {e}")
