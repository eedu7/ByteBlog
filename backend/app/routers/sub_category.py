from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud.sub_category import SubCategoryCRUD
from app.dependencies import (AuthenticationRequired, CRUDProvider,
                              get_current_user)
from app.models import User
from app.schemas.sub_category import (CreateSubCategoryRequest,
                                      UpdateSubCategoryRequest)

router = APIRouter()


@router.get("/")
async def get_sub_categories(
    skip: int = 0,
    limit: int = 100,
    crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud),
):
    return await crud.get_all_sub_categories(skip=skip, limit=limit)


@router.get("/{uuid}")
async def get_sub_category(
    uuid: UUID, crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud)
):
    sub_category = await crud.get_sub_category_by_uuid(uuid)
    return {"message": "ok", "sub_category": sub_category}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthenticationRequired)],
)
async def create_sub_category(
    data: CreateSubCategoryRequest,
    current_user: User = Depends(get_current_user),
    crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud),
):
    sub_category = await crud.create_sub_category(data.model_dump(), current_user.uuid)
    return {"message": "ok", "sub_category": sub_category}


@router.patch(
    "/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthenticationRequired)],
)
async def update_sub_category(
    uuid: UUID,
    data: UpdateSubCategoryRequest,
    current_user: User = Depends(get_current_user),
    crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud),
):
    data = data.model_dump(exclude_none=True)

    await crud.update_sub_category(
        data, sub_category_uuid=uuid, user_uuid=current_user.uuid
    )


@router.delete(
    "/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthenticationRequired)],
)
async def delete_sub_category(
    uuid: UUID, crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud)
):
    await crud.delete_sub_category(uuid)
