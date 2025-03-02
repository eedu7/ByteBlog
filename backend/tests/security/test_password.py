import pytest

from app.exceptions import BadRequestException
from app.utils import PasswordHandler


def test_password_hashing():
    """Test if passwords are hashed correctly and not equal to the original password."""
    password = "password123"
    hashed_password = PasswordHandler.hash_password(password)

    assert isinstance(hashed_password, str)
    assert hashed_password != ""
    assert hashed_password != password


def test_password_verification():
    """Test if password verification correctly matches hashed passwords."""
    password = "password123"
    hashed_password = PasswordHandler.hash_password(password)
    assert PasswordHandler.verify_password(password, hashed_password)
    incorrect_password = "wrongpassword"
    assert not PasswordHandler.verify_password(incorrect_password, hashed_password)


def test_empty_password_hashing():
    """Ensure that an empty password raises an exception when hashing."""
    with pytest.raises(
        BadRequestException, match="Password must be a non-empty string."
    ):
        PasswordHandler.hash_password("")


def test_empty_password_verification():
    """Ensure that an empty password raises an exception when verifying."""
    hashed_password = PasswordHandler.hash_password("validpassword")

    with pytest.raises(
        BadRequestException, match="Password must be a non-empty string."
    ):
        PasswordHandler.verify_password("", hashed_password)


def test_empty_hashed_password_verification():
    """Ensure that an empty hashed password raises an exception."""
    with pytest.raises(
        BadRequestException, match="Hashed password must be a valid non-empty string."
    ):
        PasswordHandler.verify_password("validpassword", "")


def test_invalid_password_type_hashing():
    """Ensure that non-string values raise an exception when hashing."""
    invalid_passwords = [None, 123, 4.56, [], {}, True]

    for invalid_password in invalid_passwords:
        with pytest.raises(
            BadRequestException, match="Password must be a non-empty string."
        ):
            PasswordHandler.hash_password(invalid_password)


def test_invalid_password_type_verification():
    """Ensure that non-string values raise an exception when verifying passwords."""
    hashed_password = PasswordHandler.hash_password("validpassword")
    invalid_passwords = [None, 123, 4.56, [], {}, True]

    for invalid_password in invalid_passwords:
        with pytest.raises(
            BadRequestException, match="Password must be a non-empty string."
        ):
            PasswordHandler.verify_password(invalid_password, hashed_password)


def test_invalid_hashed_password_type_verification():
    """Ensure that non-string hashed passwords raise an exception."""
    invalid_hashed_passwords = [None, 123, 4.56, [], {}, True]

    for invalid_hashed in invalid_hashed_passwords:
        with pytest.raises(
            BadRequestException,
            match="Hashed password must be a valid non-empty string.",
        ):
            PasswordHandler.verify_password("validpassword", invalid_hashed)


def test_different_hashed_passwords():
    """Ensure that hashing the same password twice produces different hashes (bcrypt salt uniqueness)."""
    password = "securepassword"
    hashed_password1 = PasswordHandler.hash_password(password)
    hashed_password2 = PasswordHandler.hash_password(password)

    assert (
        hashed_password1 != hashed_password2
    )  # Hashes should be different due to bcrypt salting


def test_password_verification_with_modified_hash():
    """Ensure that modifying even a single character in the hashed password results in verification failure."""
    password = "securepassword"
    hashed_password = PasswordHandler.hash_password(password)

    modified_hash = hashed_password[:-1] + (
        "X" if hashed_password[-1] != "X" else "Y"
    )  # Slight modification

    assert not PasswordHandler.verify_password(password, modified_hash)
