from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud.post_category import PostCategoryCRUD
from app.dependencies import AuthenticationRequired, CRUDProvider
from app.schemas.post_category import (CreatePostCategoryRequest,
                                       UpdatePostCategoryRequest)

router = APIRouter()


@router.get("/")
async def get_post_categories(
    skip: int = 0,
    limit: int = 100,
    crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud),
):
    return await crud.get_all_post_categories(skip=skip, limit=limit)


@router.get("/by-post/{uuid}")
async def get_post_categories_by_post_uuid(
    post_uuid: UUID,
    skip: int = 0,
    limit: int = 100,
    crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud),
):
    return await crud.get_all_post_categories_by_post_uuid(
        post_uuid=post_uuid, skip=skip, limit=limit
    )


@router.get("/{uuid}")
async def get_post_category(
    uuid: UUID, crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud)
):
    return await crud.get_post_category_by_uuid(uuid)


@router.post(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    status_code=status.HTTP_201_CREATED,
)
async def create_post_category(
    data: CreatePostCategoryRequest,
    crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud),
):
    return await crud.create_post_category(data.model_dump())


@router.patch("/{uuid}", dependencies=[Depends(AuthenticationRequired)])
async def update_post_category(
    uuid: UUID,
    data: UpdatePostCategoryRequest,
    crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud),
):
    return await crud.update_post_category(
        data.model_dump(exclude_none=True),
        post_category_uuid=uuid,
    )


@router.delete("/{uuid}", dependencies=[Depends(AuthenticationRequired)])
async def delete_post_category(
    uuid: UUID, crud: PostCategoryCRUD = Depends(CRUDProvider.get_post_category_crud)
):
    return await crud.delete_post_category(uuid)
