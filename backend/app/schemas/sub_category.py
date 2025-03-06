from uuid import UUID

from pydantic import BaseModel, Field


class SubCategoryBase(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Name of the sub category"
    )
    category_id: UUID = Field(..., description="Category UUID")


class CreateSubCategoryRequest(SubCategoryBase):
    pass


class UpdateSubCategoryRequest(SubCategoryBase):
    pass


class SubCategoryResponse(SubCategoryBase):
    uuid: UUID = Field(..., description="Sub category UUID")

    class Config:
        form_attributes = True
