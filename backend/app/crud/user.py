from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.exceptions import (BadRequestException, NotFoundException,
                            UnauthorizedException)
from app.models import User
from app.utils import PasswordHandler


class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        try:
            return await super().get_by("email", email, unique=True)
        except Exception as e:
            raise BadRequestException(e)

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

        # TODO: Create the JWT token
