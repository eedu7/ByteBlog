from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

user_router = APIRouter()


@user_router.post("/")
async def register_user():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Register User API",
        },
    )
