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
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        try:
            return await super().get_by("email", email, unique=True)
        except Exception as e:
            raise BadRequestException(e)

    async def get_by_uuid(self, uuid: UUID) -> User | None:
        return await super().get_by("uuid", uuid, unique=True)

    async def register(self, email: str, password: str, username: str) -> User:
        user = await self.get_by_email(email)
        if user:
            raise BadRequestException("User already exists")

        hashed_password = PasswordHandler.hash(password)

        user = await super().create(
            {"username": username, "email": email, "password": hashed_password}
        )
        return user

    async def login(self, email: str, password: str):
        user = await self.get_by_email(email)

        if not user:
            raise NotFoundException("User not found")

        if not PasswordHandler.verify(password, user.password):
            raise UnauthorizedException("Invalid credentials")

        payload = {
            "uuid": str(user.uuid),
            "email": user.email,
            "username": user.username,
        }

        return self._token(payload)

    def _token(self, payload: Dict[str, Any]) -> Token:
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
