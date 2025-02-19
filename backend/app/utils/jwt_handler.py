from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict
from uuid import uuid4

from app.config import config
from app.exceptions import CustomException


class JWTDecodeError(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    message = "Invalid token"


class JWTExpiredError(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    message = "Expired token"


class JWTHandler:
    secret_key = config.JWT_SECRET_KEY
    algorithm = config.JWT_ALGORITHM

    @staticmethod
    def encode(payload: dict, expire_in_min: int = 60) -> str:
        time_of_encoding = datetime.now(UTC)
        expire = time_of_encoding + timedelta(expire_in_min)

        jti = str(uuid4())
        payload.update({"exp": expire, "jti": jti, "iat": time_of_encoding})
        # TODO: return the jwt token

    @staticmethod
    def decode(token: str) -> Dict[str, Any]:
        # # TODO: logic of decoding token
        pass
