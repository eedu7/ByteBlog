from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.crud.post import PostCRUD
from app.dependencies import (AuthenticationRequired, CRUDProvider,
                              get_current_user)
from app.models import User
from app.schemas.post import PostCreateRequest, PostCreateResponse

router = APIRouter()


@router.get("/")
async def get_posts(skip: int = 0, limit: int = 100):
    return JSONResponse(
        status_code=200,
        content={
            "message": "ok",
            "posts": [
                {
                    "title": "Post 1",
                    "content": "This is the content of post 1",
                    "author": "Author 1",
                },
                {
                    "title": "Post 2",
                    "content": "This is the content of post 2",
                    "author": "Author 2",
                },
                {
                    "title": "Post 3",
                    "content": "This is the content of post 3",
                    "author": "Author 3",
                },
            ],
        },
    )


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

    return PostCreateResponse(message="Post created successfully.", post=post)
