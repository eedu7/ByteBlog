from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash(password: str) -> str:
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        return PasswordHandler.pwd_context.verify(password, hashed_password)
