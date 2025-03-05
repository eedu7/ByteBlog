from fastapi import APIRouter
from fastapi.responses import JSONResponse

# from app.crud.post import PostCRUD
# from app.dependencies import get_post_curd, AuthenticationRequired, get_current_user


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


# @router.post("/")
# async def create_post(): ...
