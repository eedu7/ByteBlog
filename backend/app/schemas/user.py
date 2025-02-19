from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    email: EmailStr = Field(
        ..., description="User email address", examples=["john.doe@example.com"]
    )
    username: str = Field(..., description="User username", examples=["john.doe"])
    uuid: UUID = Field(..., description="User UUID")
