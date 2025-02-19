from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    password: str = Field(..., description="User password", examples=["Password@123"])


class RegisterUserRequest(LoginUserRequest):
    username: str = Field(..., description="User username", examples=["john.doe"])


class UserResponse(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    username: str = Field(..., description="User username", examples=["john.doe"])
    uuid: UUID = Field(..., description="User UUID")
