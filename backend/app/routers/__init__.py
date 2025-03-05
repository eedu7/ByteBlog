from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from . import auth, category, posts, users

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/user", tags=["User"])
router.include_router(category.router, prefix="/category", tags=["Category"])
router.include_router(posts.router, prefix="/post", tags=["Post"])


@router.get("/", tags=["Health"])
async def index():
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "OK"})
