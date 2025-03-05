from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import Post


class PostCRUD(BaseCRUD[Post]):
    """
    Post-specific CRUD operations in the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the PostCRUD class with the provided async session and Post Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=Post, session=session)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """
        Get all posts from the database.

        Args:
            skip (int, optional): The number of posts to skip. Defaults to 0.
            limit (int, optional): The number of posts to return. Defaults to 100.

        Returns:
            List[Post]: A list of posts.
            
        Raises:
            NotFoundException: If there are no records.
            BadRequestException: If there is an error fetching the records.
        """
        try:
            posts = await self.get_by(skip=skip, limit=limit)
            if not posts:
                raise NotFoundException("No posts found.")
            return posts
        except Exception as e:
            raise BadRequestException(f"Exception on fetching post records. {e}")
