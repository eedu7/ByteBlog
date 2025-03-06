from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class CreatePostCategoryRequest(BaseModel):
    post_uuid: UUID = Field(..., decsription="Post UUID")
    category_uuid: UUID = Field(..., description="Category UUID")
    sub_category_uuid: List[UUID] | UUID = Field(
        ..., description="List of Sub-Categories UUID or a UUID"
    )


class UpdatePostCategoryRequest(BaseModel):
    post_uuid: UUID | None = Field(None, decsription="Post UUID")
    category_uuid: UUID | None = Field(None, description="Category UUID")
    sub_category_uuid: UUID | None = Field(None, description="SubCategory UUID")
