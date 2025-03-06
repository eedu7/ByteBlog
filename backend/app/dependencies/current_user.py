from fastapi import Depends, Request

from app.crud import UserCRUD
from app.dependencies.crud import CRUDProvider


async def get_current_user(
    request: Request, user_crud: UserCRUD = Depends(CRUDProvider.get_user_crud)
):
    return await user_crud.get_by_uuid(request.user.uuid)
