from typing import Tuple
from uuid import UUID

from jose import JWTError
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.schemas.user import CurrentUser
from app.utils import JWTHandler


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()
        authorization = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = JWTHandler.decode(token)
            user_uuid = payload.get("uuid")
        except JWTError:
            return False, current_user
        current_user.uuid = UUID(user_uuid)
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
