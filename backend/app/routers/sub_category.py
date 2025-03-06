from uuid import UUID

from fastapi import APIRouter, Depends

from app.crud.sub_category import SubCategory, SubCategoryCRUD
from app.dependencies import CRUDProvider

router = APIRouter()


@router.get("/")
async def get_sub_categories(
    skip: int = 0,
    limit: int = 100,
    crud: SubCategoryCRUD = Depends(CRUDProvider.get_sub_category_crud),
):
    return await crud.get_all_sub_categories(skip=skip, limit=limit)


@router.get("/{uuid}")
async def get_sub_category(uuid: UUID):
    return {
        "message": "ok",
        "sub_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "sub_category_1",
        },
    }


@router.post("/")
async def create_sub_category():
    return {
        "message": "ok",
        "sub_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "sub_category_1",
        },
    }


@router.put("/{uuid}")
async def update_sub_category(uuid: UUID):
    return {
        "message": "ok",
        "sub_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "sub_category_1",
        },
    }


@router.delete("/{uuid}")
async def delete_sub_category(uuid: UUID):
    return {
        "message": "ok",
        "sub_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "sub_category_1",
        },
    }
