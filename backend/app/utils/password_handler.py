from passlib.context import CryptContext

from app.exceptions import BadRequestException


class PasswordHandler:
    """
    A utility class for handling password hashing and verification.

    This class uses the `passlib` library with the `bcrypt` hashing algorithm
    to securely hash password and verify them.

    Attributes:
        pwd_context (CryptContext): A configured instance of CryptContext that
        handles password hashing and verification.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash a plain-text password using the bcrypt algorithm.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The hashed password, which can be stored securely.
        """
        if not isinstance(password, str) or not password.strip():
            raise BadRequestException("Password must be a non-empty string.")
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """
        Verify whether a given plain-text password matches a hashed password.

        Args:
            password (str): The plain-text password to verify.
            hashed_password (str): The previously hashed password to compare.

        Returns:
            bool: `True` if the password matches the hash, `False` otherwise.
        """
        if not isinstance(password, str) or not password.strip():
            raise BadRequestException("Password must be a non-empty string.")
        if not isinstance(hashed_password, str) or not hashed_password.strip():
            raise BadRequestException(
                "Hashed password must be a valid non-empty string."
            )
        return cls.pwd_context.verify(password, hashed_password)
