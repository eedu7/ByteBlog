from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import \
    AuthenticationMiddleware as BaseAuthenticationMiddleware
from starlette.requests import HTTPConnection


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> bool:
        authorization = conn.headers.get("Authorization")
        if not authorization:
            return False

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return False
        except ValueError:
            return False

        if not token:
            return False


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
