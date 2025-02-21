from passlib.context import CryptContext


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

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain-text password using the bcrypt algorithm.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The hashed password, which can be stored securely.
        """
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify whether a given plain-text password matches a hashed password.

        Args:
            password (str): The plain-text password to verify.
            hashed_password (str): The previously hashed password to compare.

        Returns:
            bool: `True` if the password matches the hash, `False` otherwise.
        """
        return PasswordHandler.pwd_context.verify(password, hashed_password)
