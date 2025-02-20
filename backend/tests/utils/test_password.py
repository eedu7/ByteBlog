import pytest

from app.utils import PasswordHandler


def test_password_hashing():
    password = "password"
    hashed_password = PasswordHandler.hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""
    assert hashed_password != password


def test_password_verification():
    password = "password"
    hashed_password = PasswordHandler.hash_password(password)

    assert PasswordHandler.verify_password(password, hashed_password)

    incorrect_password = "wrong_password"
    assert not PasswordHandler.verify_password(incorrect_password, hashed_password)
