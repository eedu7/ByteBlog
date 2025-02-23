from http import HTTPStatus
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions import CustomException
from app.middlewares import AuthBackend, AuthenticationMiddleware
from app.routers import router


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = HTTPStatus.UNAUTHORIZED, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code, content={"message": message, "error_code": error_code}
    )


async def exception_handler(request: Request, exc: Exception | CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


def init_router(app_: FastAPI):
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    app_.add_exception_handler(Exception, exception_handler)
    app_.add_exception_handler(CustomException, exception_handler)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware, backend=AuthBackend(), on_error=on_auth_error
        ),
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
    init_listeners(app_)
    return app_


app = create_app()
