from fastapi import APIRouter, Depends, status

from app.crud import UserCRUD
from app.dependencies import get_user_crud

user_router = APIRouter()


@user_router.get("/")
async def register_user(user_crud: UserCRUD = Depends(get_user_crud)):
    pass
