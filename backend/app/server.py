from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware

from app.middlewares import AuthBackend, AuthenticationMiddleware
from app.routers import router


def init_router(app_: FastAPI):
    app_.include_router(router)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
        )
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Byte Blog",
        description="Byte Blog is a simple blogging platform to share and read blog posts.",
        version="1.0.0",
        middleware=make_middleware(),
    )
    init_router(app_)
    return app_


app = create_app()
