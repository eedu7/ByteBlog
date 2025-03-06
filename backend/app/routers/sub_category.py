from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_sub_categories():
    return {
        "message": "ok",
        "sub_categories": [
            {"name": "sub_category_1"},
            {"name": "sub_category_2"},
            {"name": "sub_category_3"},
        ],
    }


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
