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
