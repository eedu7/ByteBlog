from fastapi import APIRouter, Depends, status

from app.crud import UserCRUD
from app.dependencies import get_user_crud
from app.schemas.auth import (AuthResponse, LoginUserRequest,
                              RegisterUserRequest)

auth_router = APIRouter()


@auth_router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    data: RegisterUserRequest, user_crud: UserCRUD = Depends(get_user_crud)
):
    user_data = data.model_dump()
    user = await user_crud.register(**user_data)
    token = await user_crud.login(user_data["email"], user_data["password"])
    return {"token": token, "user": user}


# NOTE: Response model of this should be similar to the register
@auth_router.post("/login", response_model=AuthResponse)
async def login(data: LoginUserRequest, user_crud: UserCRUD = Depends(get_user_crud)):
    login_data = data.model_dump()
    token = await user_crud.login(**login_data)
    user = await user_crud.get_by_email(login_data.get("email"))

    return {"token": token, "user": user}


@auth_router.post("/logout")
async def logout():
    # TODO: Add the logout logic
    pass
