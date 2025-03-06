from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import SubCategory


class SubCategoryCRUD(BaseCRUD[SubCategory]):
    """
    SubCategory-specific CRUD operations in the database.
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
        sub_categories = await self.get_by(skip=skip, limit=limit)
        if len(sub_categories) == 0 and isinstance(sub_categories, list):
            raise NotFoundException("No sub-categories found.")
        return sub_categories

    async def get_sub_category_by_uuid(self, sub_category_uuid: UUID) -> SubCategory:
        sub_category = await self.get_by_uuid(sub_category_uuid)

        if not sub_category:
            raise NotFoundException(f"No sub-category found by the UUID of: {e}")
        return sub_category

    async def create_sub_category(
        self, data: Dict[str, Any], user_uuid: UUID
    ) -> SubCategory:
        data.update({"created_by": user_uuid})
        try:
            sub_category = await self.create(data)
            return sub_category
        except Exception as e:
            raise BadRequestException(f"Exception on creating a new sub-category: {e}")

    async def update_sub_category(
        self, data: Dict[str, Any], sub_category_uuid: UUID, user_uuid: UUID
    ):
        data.update({"updated_by": user_uuid})
        sub_category = await self.get_sub_category_by_uuid(sub_category_uuid)
        try:
            updated = await self.update(sub_category, data)
            if updated:
                return True
            return False
        except Exception as e:
            raise BadRequestException(f"Exception on updated sub-category: {e}")

    async def delete_sub_category(self, sub_category_uuid: UUID):
        sub_category = await self.get_sub_category_by_uuid(sub_category_uuid)
        try:
            deleted = await self.delete(sub_category)
            if deleted:
                return True
            return False
        except Exception as e:
            raise BadRequestException(f"Exception on deleting sub-category: {e}")
