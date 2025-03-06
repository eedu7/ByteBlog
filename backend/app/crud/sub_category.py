from typing import Any, Dict
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

    async def get_all_sub_categories(self, *, skip: int = 0, limit: int = 100):
        sub_categories = await self.get_by(skip=skip, limit=limit)
        if len(sub_categories) == 0 and isinstance(sub_categories, list):
            raise NotFoundException("No sub-categories found.")
        return sub_categories

    async def get_sub_category_by_uuid(self, sub_category_uuid: UUID): ...

    async def create_sub_category(
        self, name: str, category_id: UUID, user_uuid: UUID
    ): ...

    async def update_sub_category(self, data: Dict[str, Any], user_uuid: UUID): ...

    async def delete_sub_category(self, uuid: UUID): ...
