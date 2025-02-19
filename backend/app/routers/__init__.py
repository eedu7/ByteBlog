from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .auth import auth_router
from .users import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/user", tags=["User"])


@router.get("/")
async def index():
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "OK"})
