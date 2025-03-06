from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_post_categories():
    return {
        "message": "ok",
        "post_categories": [
            {"name": "post_category_1"},
            {"name": "post_category_2"},
            {"name": "post_category_3"},
        ],
    }


@router.get("/{uuid}")
async def get_post_category():
    return {
        "message": "ok",
        "post_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "post_category_1",
        },
    }


@router.post("/")
async def create_post_category():
    return {
        "message": "ok",
        "post_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "post_category_1",
        },
    }


@router.put("/{uuid}")
async def update_post_category():
    return {
        "message": "ok",
        "post_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "post_category_1",
        },
    }


@router.delete("/{uuid}")
async def delete_post_category():
    return {
        "message": "ok",
        "post_category": {
            "uuid": "12ff631d-533c-45b3-9fad-8cabce6a9d6f",
            "name": "post_category_1",
        },
    }
