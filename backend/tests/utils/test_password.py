import pytest

from app.utils import PasswordHandler


def test_password_hashing():
    password = "password"
    hashed_password = PasswordHandler.hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != ""
    assert hashed_password != password


def test_password_verification():
    password = "password"
    hashed_password = PasswordHandler.hash(password)

    assert PasswordHandler.verify(password, hashed_password)

    incorrect_password = "wrong_password"
    assert not PasswordHandler.verify(incorrect_password, hashed_password)
