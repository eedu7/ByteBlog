from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_tables
from app.routers import router


def init_router(app_: FastAPI):
    app_.include_router(router)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await create_tables()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(title="Byte Blog", version="1.0.0", lifespan=lifespan)
    init_router(app_)
    return app_


app = create_app()
