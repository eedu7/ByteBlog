from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models import Category


class CategoryCRUD(BaseCRUD[Category]):
    """
    Category-specific CRUD operations for managing user accounts in the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the CategoryCRUD class with the provided async session and Post Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=Category, session=session)
