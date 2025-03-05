from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import BadRequestException, NotFoundException
from app.models import Post, User


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

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
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

    async def get_post_by_uuid(self, uuid) -> Post:
        """
        Get a post by its UUID.

        Args:
            uuid: The UUID of the post to fetch.

        Returns:
            Post: The post record.

        Raises:
            NotFoundException: If there is no post found.
            BadRequestException: If there is an error fetching the post record.
        """
        try:
            post = await self.get_by_uuid(uuid)
            if not post:
                raise NotFoundException("No post found.")
            return post
        except Exception as e:
            raise NotFoundException(f"Exception on fetching post record. {e}")

    async def create_post(self, attributes: Dict[str, Any]) -> Post:
        """
        Create a new post in the database.

        Args:
            attributes (Dict[str, Any]): The attributes of the post to be created.

        Returns:
            Post: The created post.

            BadRequestException: If there is an error creating the post.
        """
        try:
            post = await self.create(attributes)
            return post
        except Exception as e:
            raise BadRequestException(f"Exception on creating post. {e}")

    async def update_post(self, uuid: UUID, attributes: Dict[str, Any]) -> Post:
        """
        Update a post in the database.

        Args:
            uuid: The UUID of the post to update.
            attributes (Dict[str, Any]): The attributes to update.

        Returns:
            Post: The updated post.

        Raises:
            NotFoundException: If there is no post found.
            BadRequestException: If there is an error updating the post.
        """
        try:
            post = await self.get_post_by_uuid(uuid)
            post = await self.update(post, attributes)
            return post
        except Exception as e:
            raise BadRequestException(f"Exception on updating post. {e}")

    async def delete_post(self, uuid: UUID) -> None:
        """
        Delete a post from the database.

        Args:
            uuid: The UUID of the post to delete.

        Raises:
            NotFoundException: If there is no post found.
            BadRequestException: If there is an error deleting the post.
        """
        try:
            post = await self.get_post_by_uuid(uuid)
            await self.delete(post)
        except Exception as e:
            raise BadRequestException(f"Exception on deleting post. {e}")
