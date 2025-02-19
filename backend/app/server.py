from fastapi import FastAPI

from app.routers import router


def init_router(app_: FastAPI):
    app_.include_router(router)


def create_app() -> FastAPI:
    app_ = FastAPI(title="Byte Blog", version="1.0.0")
    init_router(app_)
    return app_


app = create_app()
