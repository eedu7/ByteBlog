from fastapi import Depends, Request

from app.crud import UserCRUD
from app.dependencies import get_user_crud


async def get_current_user(
    request: Request, user_crud: UserCRUD = Depends(get_user_crud)
):
    return await user_crud.get_by_uuid(request.user.uuid)
