from pydantic import BaseModel, EmailStr, Field

from .token import Token
from .user import UserResponse


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    password: str = Field(..., description="User password", examples=["Password@123"])


class RegisterUserRequest(LoginUserRequest):
    username: str = Field(..., description="User username", examples=["john.doe"])


class LogoutUserRequest(BaseModel):
    access_token: str = Field(..., description="Access token of the being log out.")


class ForgotPasswordRequest(BaseModel):
    old_password: str = Field(
        ..., description="User's old password", examples=["Password@123"]
    )
    new_password: str = Field(
        ..., description="User's new password", examples=["Password@1234"]
    )


class AuthResponse(BaseModel):
    token: Token
    user: UserResponse
