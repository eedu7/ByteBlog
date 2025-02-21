from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.crud import UserCRUD
from app.dependencies import get_user_crud
from app.schemas.auth import (AuthResponse, LoginUserRequest,
                              LogoutUserRequest, RegisterUserRequest)

auth_router = APIRouter()


@auth_router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    data: RegisterUserRequest, user_crud: UserCRUD = Depends(get_user_crud)
):
    """
    Registers a new user and returns an authentication token along with user details.

    Args:
        data (RegisterUserRequest): The user registration details (email, password and username).
            Example:
                {
                    "email": "john.doe@example.com",
                    "username": "john.doe",
                    "password": "secure_password
                }
        user_crud (UserCRUD): The dependency-injected UserCRUD instance for handling database operations.

    Returns:
        AuthResponse: A response containing the authentication token and user details.
            Example:
                {
                    "token": {
                        "access_token": "<ACCESS TOKEN>",
                        "refresh_token": "<REFRESH TOKEN>",
                        "expires_in": 60,
                        "token_type": "bearer"
                    },
                    "user": {
                        "uuid": "uuid",
                        "email": "john.doe@example.com",
                        "username": "john.doe"
                    }
                }
    """
    user_data = data.model_dump()
    user = await user_crud.register(**user_data)
    token = await user_crud.login(user_data["email"], user_data["password"])
    return {"token": token, "user": user}


@auth_router.post("/login", response_model=AuthResponse)
async def login(data: LoginUserRequest, user_crud: UserCRUD = Depends(get_user_crud)):
    """
    Authenticates a user and returns an authentication token along with the user details.

    Args:
        data (LoginUserRequest): The user's login credentials (email and password).
            Example:
                {
                    "email": "john.doe@example.com",
                    "password": "secure_password"
                }
        user_crud (UserCRUD): The dependency-injected UserCRUD instance for handling authentication

    Returns:
        AuthResponse: A response containing the authentication token and user details.
            Example:
                {
                    "token": {
                        "access_token": "<ACCESS TOKEN>",
                        "refresh_token": "<REFRESH TOKEN>",
                        "expires_in": 60,
                        "token_type": "bearer"
                    },
                    "user": {
                        "uuid": "uuid",
                        "email": "john.doe@example.com",
                        "username": "john.doe"
                    }
                }
    """
    login_data = data.model_dump()
    token = await user_crud.login(**login_data)
    user = await user_crud.get_by_email(login_data.get("email"))

    return {"token": token, "user": user}


@auth_router.post("/logout")
async def logout(data: LogoutUserRequest):
    """
    Logs out the current users.

    Args:
        data (LogoutUserRequest): The user access token.

    Returns:
        JSONResponse: A response confirming that the user has been successfully logged out.
    """

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User logout successfully."}
    )
