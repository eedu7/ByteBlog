from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.crud.base import BaseCRUD
from app.exceptions import (BadRequestException, NotFoundException,
                            UnauthorizedException)
from app.models import User
from app.schemas.token import Token
from app.utils import JWTHandler, PasswordHandler


class UserCRUD(BaseCRUD[User]):
    """
    User-specific CRUD operations for managing user accounts in the database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the UserCRUD class with the provided async session and User Model

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to interact with the database.
        """
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        """
        Asynchronously retrieves a user from the database by their email address.

        Args:
            email (str): The email address of the User to be retrieved.

        Returns:
            User | None: The user object if found, otherwise None
        """
        try:
            filter_ = {"email": email}
            return await self.get_by(filter_, unique=True)
        except Exception as e:
            raise BadRequestException(e)

    async def get_by_uuid(self, uuid: UUID) -> User | None:
        """
        Asynchronously retrieves a user from the database by their uuid.

        Args:
            uuid (UUID): The uuid of the User to be retrieved.

        Returns:
            User | None: The user object if found, otherwise None
        """
        try:
            filter_ = {"uuid": uuid}
            return await self.get_by(filter_, unique=True)
        except Exception as e:
            raise BadRequestException(e)

    async def get_all_users(self, skip: int = 0, limit: int = 100):
        try:
            return await self.get_by(
                skip=skip,
                limit=limit,
            )
        except Exception as e:
            raise BadRequestException(f"Exception on fetching all user. `{e}`")

    async def register(self, email: str, password: str, username: str) -> User:
        """
        Registers a new user asynchronously by hashing their password and saving
        the user data to the database.

        Args:
            email (str): The email address of the new user.
            password (str): The password of the new user.
            username (str): The username of the new user.

        Returns:
            User: The newly created User object with the hashed password

        Raises:
            BadRequestException: If a user with the same email already exists.
        """
        user = await self.get_by_email(email)
        if user:
            raise BadRequestException("User already exists")

        hashed_password = PasswordHandler.hash_password(password)

        user = await self.create(
            {"username": username, "email": email, "password": hashed_password}
        )
        return user

    async def login(self, email: str, password: str) -> Token:
        """
        Logs in a user by validating their credentials (email and password) and
        generating JWT tokens for authentication.

        Args:
            email (str): The email address of the user.
            password (str): The password provided by the user.

        Returns:
            Token: A Token object containing an access token and a refresh token.

        Raises:
            NotFoundException: If no user is found with the given email address.
            UnauthorizedException: If the password is incorrect.
        """
        user = await self.get_by_email(email)

        if not user:
            raise NotFoundException("User not found.")

        if not PasswordHandler.verify_password(password, user.password):
            raise UnauthorizedException("Invalid credentials.")

        payload = {
            "uuid": str(user.uuid),
            "email": user.email,
            "username": user.username,
        }

        return self._token(payload)

    async def forgot_password(
        self, uuid: UUID, old_password: str, new_password: str
    ) -> User:
        """
        Updates the user password, after validation if the user exists and old password matches.

        Args:
            uuid (UUID: The uuid of the user.
            old_password (str): Old password of the user.
            new_password (str): New password to chage from old password.

        Returns:
            User: The updated user.

        Raises:
            NotFoundException: If no user is found with the given email address.
            UnauthorizedException: If the password is incorrect.
        """
        user = await self.get_by_uuid(uuid)

        if not user:
            raise NotFoundException("User not found.")

        if not PasswordHandler.verify_password(old_password, user.password):
            raise UnauthorizedException("Invalid credentials.")

        hashed_new_password = PasswordHandler.hash_password(new_password)

        updated_user = await self.update(
            user,
            {
                "password": hashed_new_password,
            },
        )
        return updated_user

    def _token(self, payload: Dict[str, Any]) -> Token:
        """
        Generates JWT tokens (access and refresh) for the user based on the
        provided payload data.

        Args:
            payload (Dict[str, Any]): The payload data to be included in the JWT token.

        Returns:
            Token: A Token object containing the access token, refresh token, token type (default: `bearer`) and token expiration time.
        """
        access_token = JWTHandler.encode(
            payload, config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"sub": "refresh_token"})
        refresh_token = JWTHandler.encode(
            payload, config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        )
