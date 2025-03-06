from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud.category import CategoryCRUD
from app.dependencies import (AuthenticationRequired, CRUDProvider,
                              get_current_user)
from app.models import User
from app.schemas.category import (CategoryResponse, CreateCategoryRequest,
                                  UpdateCategoryRequest)

router = APIRouter()


@router.get("/")
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    crud: CategoryCRUD = Depends(CRUDProvider.get_category_crud),
):
    return await crud.get_all_categories(skip=skip, limit=limit)


@router.get("/{uuid}")
async def get_category(
    uuid: UUID, crud: CategoryCRUD = Depends(CRUDProvider.get_category_crud)
):
    return await crud.get_category_by_uuid(uuid)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
    dependencies=[Depends(AuthenticationRequired)],
)
async def create_category(
    data: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),
    crud: CategoryCRUD = Depends(CRUDProvider.get_category_crud),
):
    category = await crud.create_category(name=data.name, user_uuid=current_user.uuid)
    return category


@router.put(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthenticationRequired)],
)
async def update_category(
    data: UpdateCategoryRequest,
    uuid: UUID,
    current_user: User = Depends(get_current_user),
    crud: CategoryCRUD = Depends(CRUDProvider.get_category_crud),
):
    updated = await crud.update_category(
        category_uuid=uuid, user_uuid=current_user.uuid, updated_name=data.name
    )
    if updated:
        return {"message": "Category updated successfully."}
    return {"message": "Error in updating the category."}


@router.delete(
    "/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthenticationRequired)],
)
async def delete_category(
    uuid: UUID, crud: CategoryCRUD = Depends(CRUDProvider.get_category_crud)
):
    await crud.delete_category(uuid)
