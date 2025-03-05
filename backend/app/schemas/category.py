from uuid import UUID

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., title="The name of the category")


class CreateCategoryRequest(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    uuid: UUID = Field(..., description="The UUID of the category")

    class Config:
        form_attributes = True


class UpdateCategoryRequest(CategoryBase):
    pass
