from fastapi import APIRouter, Depends

from app.dependencies import AuthenticationRequired
from app.dependencies.current_user import get_current_user
from app.models import User

user_router = APIRouter()


@user_router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_current_user(current_user: User = Depends(get_current_user)):
    return {"message": "OK", "user": current_user}
