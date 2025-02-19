from fastapi import APIRouter, Depends

from app.crud import UserCRUD
from app.dependencies import get_user_crud
from app.schemas.auth import (AuthResponse, LoginUserRequest,
                              RegisterUserRequest, UserResponse)

auth_router = APIRouter()


# NOTE: Change the response model, to contain JWT token as well as user data
@auth_router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterUserRequest, user_crud: UserCRUD = Depends(get_user_crud)
):
    # TODO: logs in the user and generate the JWT token, after registration
    return await user_crud.register(**data.model_dump())


# NOTE: Response model of this should be similar to the register
@auth_router.post("/login")
async def login(data: LoginUserRequest, user_crud: UserCRUD = Depends(get_user_crud)):
    login_data = data.model_dump()
    token = await user_crud.login(**login_data)
    user = await user_crud.get_by_email(login_data.get("email"))

    return {"token": token, "user": user}


@auth_router.post("/logout")
async def logout():
    # TODO: Add the logout logic
    pass
