from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    username: str = Field(..., description="User username", examples=["john.doe"])
    uuid: UUID = Field(..., description="User UUID")


class CurrentUser(BaseModel):
    uuid: UUID | None = Field(None, description="Currently logged user's uuid")

    class Config:
        validate_assignment = True
