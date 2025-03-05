from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud.post import PostCRUD
from app.dependencies import (AuthenticationRequired, CRUDProvider,
                              get_current_user)
from app.models import User
from app.schemas.post import (PostCreateRequest, PostCreateResponse,
                              PostPartialUpdateRequest, PostUpdateRequest)

router = APIRouter()


@router.get("/")
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    crud: PostCRUD = Depends(CRUDProvider.get_post_curd),
):
    posts = await crud.get_all_posts(skip=skip, limit=limit)
    return posts


@router.get("/{uuid}")
async def get_post(uuid: UUID, crud: PostCRUD = Depends(CRUDProvider.get_post_curd)):
    return await crud.get_post_by_uuid(uuid)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthenticationRequired)],
    response_model=PostCreateResponse,
)
async def create_post(
    data: PostCreateRequest,
    crud: PostCRUD = Depends(CRUDProvider.get_post_curd),
    current_user: User = Depends(get_current_user),
):
    post_data = data.model_dump()
    post_data.update({"created_by": current_user.uuid, "updated_by": current_user.uuid})
    post = await crud.create_post(post_data)

    return {"message": "Post created successfully.", "post": post}


@router.put("/{uuid}", status_code=status.HTTP_200_OK)
async def update_post(
    uuid: UUID,
    data: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    crud: PostCRUD = Depends(CRUDProvider.get_post_curd),
):
    data = data.model_dump()
    data.update({"updated_by": current_user.uuid})
    updated_post = await crud.update_post(uuid, data)
    return {
        "message": "Post updated successfully.",
        "post": updated_post,
    }


@router.patch("/{uuid}", status_code=status.HTTP_200_OK)
async def partial_update_post(
    uuid: UUID,
    data: PostPartialUpdateRequest,
    current_user: User = Depends(get_current_user),
    crud: PostCRUD = Depends(CRUDProvider.get_post_curd),
):
    data = data.model_dump(exclude_none=True)
    data.update({"updated_by": current_user.uuid})
    updated_post = await crud.update_post(uuid, data)
    return {
        "message": "Post updated successfully.",
        "post": updated_post,
    }


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(uuid: UUID, crud: PostCRUD = Depends(CRUDProvider.get_post_curd)):
    # TODO: Make it soft delete, right now, it will be hard deleted
    await crud.delete_post(uuid)


@router.post("/delete/multiple")
async def delete_multiple_post():
    pass
