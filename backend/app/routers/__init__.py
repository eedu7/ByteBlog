from http import HTTPStatus

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from . import auth, category, post_category, posts, sub_category, users

router = APIRouter()


@router.get("/", tags=["Health"], status_code=status.HTTP_200_OK)
async def index():
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "OK"})


router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/user", tags=["User"])
router.include_router(category.router, prefix="/category", tags=["Category"])
router.include_router(
    sub_category.router, prefix="/sub-category", tags=["Sub Category"]
)
router.include_router(posts.router, prefix="/post", tags=["Post"])
router.include_router(
    post_category.router, prefix="/post-category", tags=["Post Category"]
)
