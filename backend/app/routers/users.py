from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.crud import UserCRUD
from app.dependencies import AuthenticationRequired, get_user_crud
from app.dependencies.current_user import get_current_user
from app.exceptions import BadRequestException
from app.models import User
from app.schemas.user import (PartialUpdateUserRequest, UpdateUserRequest,
                              UserResponse)

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


@user_router.put(
    "/{uuid}",
)
async def update_user_profile(
    uuid: UUID, data: UpdateUserRequest, user_crud: UserCRUD = Depends(get_user_crud)
):
    user_attr = data.model_dump()
    updated = await user_crud.update_user_profile(uuid, attributes=user_attr)

    if updated:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Updated user successfully.",
                "api": f"http://localhost:8000/user/{uuid}",
            },
        )
    raise BadRequestException("Error in updating user")


@user_router.patch("/{uuid}")
async def partial_update_user_profile(
    uuid: UUID,
    data: PartialUpdateUserRequest,
    user_crud: UserCRUD = Depends(get_user_crud),
):
    user_attr = data.model_dump(exclude_none=True)
    updated = await user_crud.update_user_profile(uuid, attributes=user_attr)

    if updated:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Updated user successfully.",
                "api": f"http://localhost:8000/user/{uuid}",
            },
        )
    raise BadRequestException("Error in updating user")


@user_router.delete("/{uuid}")
async def delete_user(uuid: UUID, user_crud: UserCRUD = Depends(get_user_crud)):
    await user_crud.delete_user(uuid)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User deleted successfully.",
        },
    )
