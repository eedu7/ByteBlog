from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.crud import UserCRUD
from app.dependencies import AuthenticationRequired, get_user_crud
from app.dependencies.current_user import get_current_user
from app.models import User
from app.schemas.user import UserResponse

user_router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@user_router.get(
    "/",
)
async def get_all_users(
    skip: int = 0, limit: int = 100, user_crud: UserCRUD = Depends(get_user_crud)
):
    return await user_crud.get_all_users()


@user_router.get("/user-profile", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get("/{uuid}")
async def get_user(uuid: UUID):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Get user by uuid",
            "api": f"http://localhost:8000/user/{uuid}",
        },
    )


@user_router.post(
    "/{uuid}",
)
async def update_user_profile(uuid: UUID):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Update the user",
            "api": f"http://localhost:8000/user/{uuid}",
        },
    )


@user_router.put("/{uuid}")
async def partial_update_user_profile(uuid: UUID):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Partial update the user",
            "api": f"http://localhost:8000/user/{uuid}",
        },
    )


@user_router.delete("/{uuid}")
async def delete_user(uuid: UUID):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Delete user",
            "api": f"http://localhost:8000/user/{uuid}",
        },
    )
