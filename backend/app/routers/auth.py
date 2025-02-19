from fastapi import APIRouter, Depends

from app.crud import UserCRUD
from app.dependencies import get_user_crud
from app.schemas.auth import RegisterUserRequest, UserResponse

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
async def login():
    # TODO: Add the login logic
    pass


@auth_router.post("/logout")
async def logout():
    # TODO: Add the logout logic
    pass
