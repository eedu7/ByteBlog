from fastapi import APIRouter, Depends

from app.crud import UserCRUD
from app.dependencies import get_user_crud
from app.schemas.user import RegisterUserRequest, UserResponse

user_router = APIRouter()


@user_router.post("/register", response_model=UserResponse)
async def register_user(
    data: RegisterUserRequest, user_crud: UserCRUD = Depends(get_user_crud)
):
    return await user_crud.register(**data.model_dump())
