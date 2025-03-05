from enum import StrEnum

from pydantic import BaseModel, Field


class PostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"
    ARCHIVED = "archived"


class PostCreateRequest(BaseModel):
    title: str = Field(..., examples=["Title of the post"], max_length=255)
    body: str = Field(..., examples=["This is the content of the post"])
    status: PostStatus = Field(
        default=PostStatus.DRAFT, examples=[PostStatus.DRAFT, PostStatus.PUBLISHED]
    )


class PostCreateResponse(BaseModel):
    message: str = Field(default="Post created successfully.")
    post: PostCreateRequest
