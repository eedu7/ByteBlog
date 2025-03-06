from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.base import BaseCRUD
from app.exceptions import (BadRequestException, CustomException,
                            NotFoundException)
from app.models import Post, PostCategory, SubCategory


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
            query = (
                select(Post)
                .options(
                    selectinload(Post.post_categories)
                    .selectinload(PostCategory.sub_categories)
                    .selectinload(SubCategory.category)
                )
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(query)
            posts = result.mappings().all()
            if not posts:
                raise NotFoundException("No posts found.")
            return posts
        except Exception as e:
            raise BadRequestException(f"Exception on fetching post records. {e}")

    async def get_post_by_uuid(self, uuid: UUID) -> Post:
        """
        Get a post by its UUID.

        Args:
            uuid (UUID): The UUID of the post to fetch.

        Returns:
            Post: The post record.

        Raises:
            NotFoundException: If there is no post found.
            BadRequestException: If there is an error fetching the post record.
        """
        try:
            query = (
                select(Post)
                .options(
                    selectinload(Post.post_categories)
                    .selectinload(PostCategory.sub_categories)
                    .selectinload(SubCategory.category)
                )
                .filter(Post.uuid == uuid)
            )
            result = await self.session.execute(query)
            post = result.scalar_one_or_none()
            if not post:
                raise NotFoundException("No post found.")
            return post
        except CustomException:
            raise
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
            updated = await self.update(post, attributes)
            if updated:
                return True
            return False
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
