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
        self.session = session
        super().__init__(model=Category, session=self.session)

    async def get_all_categories(
        self, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        try:
            posts = await self.get_by(skip=skip, limit=limit)
            return posts
        except Exception as e:
            raise BadRequestException(f"Exception on fetching all categories. {e}")

    async def get_category_by_uuid(self, uuid: UUID):
        try:
            category = await self.get_by_uuid(uuid)
            if not category:
                raise NotFoundException(f"No category found by uuid: {str(uuid)}")
            return category
        except Exception as e:
            raise BadRequestException(f"Exception on fetching category by uuid. {e}")

    async def create_category(self, *, name: str, user_uuid: UUID) -> Category:
        """
        Create a new category in the database.

        Args:
            name (str): The name of the category
            user_uuid (UUID): The UUID of the user, creating the category.
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
        # TODO: Make it soft delete
        category = await self.get_category_by_uuid(category_uuid)
        try:
            deleted = await self.delete(category)
            if deleted:
                return True
            return False
        except Exception as e:
            raise BadRequestException(f"Exception on deleting category. {e}")
