from fastapi import APIRouter, Depends

from app.dependencies import AuthenticationRequired
from app.dependencies.current_user import get_current_user
from app.models import User
from app.schemas.user import UserResponse

user_router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@user_router.get("/user-profile/", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user
