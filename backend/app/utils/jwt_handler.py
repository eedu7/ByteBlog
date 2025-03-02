from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict, Tuple
from uuid import uuid4

from jose import ExpiredSignatureError, JWTError, jwt

from app.config import config
from app.exceptions import CustomException


class JWTDecodeError(CustomException):
    """
    Exception raised when a JWT token cannot be decoded due to invalid format or signature.
    """

    code = HTTPStatus.UNAUTHORIZED
    message = "Invalid token"


class JWTExpiredError(CustomException):
    """
    Exception raised when a JWT token has expired.
    """

    code = HTTPStatus.UNAUTHORIZED
    message = "Expired token"


class JWTHandler:
    """
    A utility class for handling JSON Web Token (JWT) encoding and decoding.

    This class provides methods to generate and validate JWTs using a secret kwt and a specified algorithm. It includes built-in expiration handling to ensure security.

    Attributes:
        secret_key (str): The secret kwy used for signing JWTs.
        algorithm (str): The algorithm used for encoding and decoding JWTs.
    """

    secret_key = config.JWT_SECRET_KEY
    algorithm = config.JWT_ALGORITHM

    @classmethod
    def encode(
        cls, payload: Dict[str, Any], expire_in_min: int = 60
    ) -> Tuple[str, datetime]:
        """
        Generates a JWT with the given payload and expiration time.

        Args:
            payload (Dict[str, Any]): The data to include in the JWT.
            expire_in_min (int, optional): The expiration time in minutes. Defaults to `60`.

        Returns:
            str: The encoded JWT as string
        """
        time_of_encoding = datetime.now(UTC)
        expire = time_of_encoding + timedelta(minutes=expire_in_min)

        jti = str(uuid4())
        payload.update({"exp": expire, "jti": jti, "iat": time_of_encoding})
        return jwt.encode(payload, cls.secret_key, algorithm=cls.algorithm), expire

    @classmethod
    def decode(cls, token: str) -> Dict[str, Any]:
        """
        Decodes and verifies a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            Dict[str, Any]: The decoded payload if the token is valid.

        Raises:
            JWTExpiredError: If the token has expired.
            JWTDecodeError: If the token is invalid or cannot be decoded.
        """
        try:
            return jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
        except ExpiredSignatureError:
            raise JWTExpiredError()
        except JWTError as e:
            raise JWTDecodeError() from e

    @classmethod
    def decode_expired(cls, token: str) -> Dict[str, Any]:
        """
        Decodes a expired JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            Dict[str, Any]: The decoded payload.

        Raises:
            JWTDecodeError: If the token is invalid or cannot be decoded.
        """
        try:
            return jwt.decode(
                token,
                cls.secret_key,
                algorithms=[cls.algorithm],
                options={"verify_exp": False},
            )
        except JWTError as e:
            raise JWTDecodeError() from e
