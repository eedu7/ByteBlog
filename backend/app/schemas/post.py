from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class PostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"
    ARCHIVED = "archived"


class PostBase(BaseModel):
    title: str = Field(..., examples=["Title of the post"], max_length=255)
    body: str = Field(..., examples=["This is the content of the post"])
    status: PostStatus = Field(
        default=PostStatus.DRAFT, examples=[PostStatus.DRAFT, PostStatus.PUBLISHED]
    )


class PostCreateRequest(PostBase):
    pass


class PostUpdateRequest(PostBase):
    pass


class PostPartialUpdateRequest:
    title: str | None = Field(None, examples=["Title of the post"], max_length=255)
    body: str | None = Field(None, examples=["This is the content of the post"])
    status: PostStatus | None = Field(
        None, examples=[PostStatus.DRAFT, PostStatus.PUBLISHED]
    )


class PostUpdateStatusRequest(BaseModel):
    status: PostStatus = Field(..., examples=[PostStatus.DRAFT, PostStatus.PUBLISHED])


class PostResponse(PostBase):
    uuid: str | UUID = Field(..., description="Post UUID")

    class Config:
        form_attributes = True


class PostCreateResponse(BaseModel):
    message: str = Field(default="Post created successfully.")
    post: PostResponse

    class Config:
        form_attributes = True
