from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from jose import JWTError, jwt

from app.utils.jwt_handler import JWTDecodeError, JWTHandler


class MockConfig:
    JWT_SECRET_KEY = "Secret-Key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_MINUTES = 10


@pytest.fixture
def mock_config():
    return MockConfig()


@pytest.fixture
def mock_payload():
    return {
        "uuid": "92b6cefe-d64f-4660-a53b-dfb2a0cb2147",
        "email": "john.doe@example.com",
        "username": "john.doe",
        "jti": "92b6cefe-d64f-4660-a53b-dfb2a0cb2147",
    }


@pytest.fixture
def mock_token(mock_payload, mock_config):
    time_of_encoding = datetime.now(UTC)
    expire = time_of_encoding + timedelta(mock_config.JWT_EXPIRE_MINUTES)
    payload = mock_payload.copy()
    payload.update({"exp": expire})
    return jwt.encode(
        payload, mock_config.JWT_SECRET_KEY, algorithm=mock_config.JWT_ALGORITHM
    )


@pytest.fixture
def mock_expired_token(mock_payload, mock_config):
    time_of_encoding = datetime.now(UTC)
    expire = (
        time_of_encoding
        - timedelta(mock_config.JWT_EXPIRE_MINUTES)
        - timedelta(seconds=10)
    )
    payload = mock_payload.copy()
    payload.update({"exp": expire})
    return jwt.encode(
        payload, mock_config.JWT_SECRET_KEY, algorithm=mock_config.JWT_ALGORITHM
    )


@pytest.fixture
def mock_decode_token(mock_payload, mock_config):
    return jwt.encode(
        mock_payload, mock_config.JWT_SECRET_KEY, algorithm=mock_config.JWT_ALGORITHM
    )


@pytest.fixture
def mock_handler(mock_config):
    jwt_handler = JWTHandler
    jwt_handler.secret_key = mock_config.JWT_SECRET_KEY
    jwt_handler.algorithm = mock_config.JWT_ALGORITHM

    return jwt_handler


class TestJWTHandler:
    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_encode(self, mock_payload, mock_handler, mock_config):
        token = mock_handler.encode(mock_payload, mock_config.JWT_EXPIRE_MINUTES)
        assert token is not None
        assert isinstance(token, str)

    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_decode(self, mock_token, mock_payload, mock_handler):
        decoded = mock_handler.decode(mock_token)
        assert decoded is not None
        assert isinstance(decoded, dict)
        assert decoded.pop("exp") is not None
        assert decoded == mock_payload

    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_decode_error(self, mock_token, mock_handler):
        with pytest.raises(JWTDecodeError):
            with patch.object(jwt, "decode", side_effect=JWTError):
                mock_handler.decode(mock_token)

    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_decode_expired(self, mock_expired_token, mock_handler):
        decoded = mock_handler.decode_expired(mock_expired_token)
        assert decoded is not None
        assert isinstance(decoded, dict)

    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_decode_error(self, mock_token, mock_handler):
        with pytest.raises(JWTDecodeError):
            with patch.object(jwt, "decode", side_effect=JWTError):
                mock_handler.decode(mock_token)

    @patch("app.utils.jwt_handler.config", MagicMock(return_value=mock_config))
    def test_decode_expired_error(self, mock_handler):
        with pytest.raises(JWTDecodeError):
            with patch.object(jwt, "decode", side_effect=JWTError):
                mock_handler.decode_expired(mock_token)
