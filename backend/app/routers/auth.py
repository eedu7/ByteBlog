from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.crud import UserCRUD
from app.dependencies import AuthenticationRequired, CRUDProvider
from app.schemas.auth import (AuthResponse, LoginUserRequest,
                              LogoutUserRequest, RegisterUserRequest,
                              ResetPasswordRequest, UserResponse)

router = APIRouter()


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    data: RegisterUserRequest,
    user_crud: UserCRUD = Depends(CRUDProvider.get_user_crud),
):
    user_data = data.model_dump()
    user = await user_crud.register(**user_data)
    token = await user_crud.login(user_data["email"], user_data["password"])
    return {
        "token": token,
        "user": user,
    }


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(
    data: LoginUserRequest, user_crud: UserCRUD = Depends(CRUDProvider.get_user_crud)
):
    login_data = data.model_dump()
    token = await user_crud.login(**login_data)
    user = await user_crud.get_by_email(login_data.get("email"))
    return {
        "token": token,
        "user": user,
    }


@router.post("/logout")
async def logout(data: LogoutUserRequest):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User logout successfully.", "data": data},
    )


@router.post("/reset-password/{uuid}", dependencies=[Depends(AuthenticationRequired)])
async def reset_password(
    uuid: UUID,
    data: ResetPasswordRequest,
    user_crud: UserCRUD = Depends(CRUDProvider.get_user_crud),
):
    await user_crud.reset_password(uuid, data.old_password, data.new_password)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Password changed"}
    )
