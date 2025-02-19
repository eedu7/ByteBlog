from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models import User
from app.utils import PasswordHandler

class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        try:
            return await super().get_by("email", email, unique=True)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def register(self, email: str, password: str, username: str):
        user = await self.get_by_email(email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
        hashed_password = PasswordHandler.hash(password)
        
        user = await super().create({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        return user
    
    async def login(self, email: str, password: str):
        user = await self.get_by_email(email)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
        
        if not PasswordHandler.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # TODO: Create the JWT token