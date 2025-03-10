from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    uuid: UUID = Field(..., description="User UUID")
    username: str = Field(..., description="User username", examples=["john.doe"])
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    profile_image: str | None = Field(None, description="User profile image URL")

    class Config:
        from_attributes = True


class CurrentUser(BaseModel):
    uuid: UUID | None = Field(None, description="Currently logged user's uuid")

    class Config:
        validate_assignment = True


class UpdateUserRequest(BaseModel):
    full_name: str = Field(..., description="User full name", exampls=["John Doe"])
    bio: str = Field(
        ...,
        description="Use bio",
    )


class PartialUpdateUserRequest(BaseModel):
    full_name: str | None = Field(
        None, description="User full name", exampls=["John Doe"]
    )
    bio: str | None = Field(
        None,
        description="Use bio",
    )
