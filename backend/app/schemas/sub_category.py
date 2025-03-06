from uuid import UUID

from pydantic import BaseModel, Field


class SubCategoryBase(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the sub category"
    )
    category_uuid: UUID = Field(..., description="Category UUID")


class CreateSubCategoryRequest(SubCategoryBase):
    pass


class UpdateSubCategoryRequest(BaseModel):
    name: str | None = Field(
        None, min_length=3, max_length=50, description="Name of the sub category"
    )
    category_uuid: UUID | None = Field(None, description="Category UUID")


class SubCategoryResponse(SubCategoryBase):
    uuid: UUID = Field(..., description="Sub category UUID")

    class Config:
        form_attributes = True
