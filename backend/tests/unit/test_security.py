"""Unit tests for password hashing and JWT security in core/security.py."""

from datetime import timedelta

import jwt
import pytest

from app.core.errors import InvalidTokenError
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_does_not_contain_plaintext() -> None:
    """The generated hash must never contain the plain password in cleartext."""
    plain_password = "SuperSecretPassword123!"
    hashed = hash_password(plain_password)
    assert plain_password not in hashed
    assert len(hashed) > len(plain_password)


def test_hash_password_uses_unique_salts() -> None:
    """Two hashes of the same password must differ due to unique salts."""
    plain_password = "IdenticalPasswordToHash"
    hash1 = hash_password(plain_password)
    hash2 = hash_password(plain_password)
    assert hash1 != hash2


def test_verify_password_succeeds_with_correct_password() -> None:
    """verify_password must return True when given the correct plaintext password."""
    plain_password = "CorrectHorseBatteryStaple"
    hashed = hash_password(plain_password)
    assert verify_password(plain_password, hashed) is True


def test_verify_password_fails_with_incorrect_password() -> None:
    """verify_password must return False when given an incorrect plaintext password."""
    plain_password = "ValidPassword456"
    hashed = hash_password(plain_password)
    assert verify_password("WrongPassword999", hashed) is False


def test_verify_password_handles_malformed_hash_gracefully() -> None:
    """verify_password must return False on corrupted or invalid hashes."""
    plain_password = "AnyPassword"
    malformed_hashes = [
        "not_an_argon2_hash",
        "$argon2id$v=19$m=65536,t=3,p=4$corrupted_payload",
        "",
        "   ",
    ]
    for bad_hash in malformed_hashes:
        assert verify_password(plain_password, bad_hash) is False


def test_jwt_carries_subject_and_role_and_timestamps() -> None:
    """create_access_token must embed sub, role, iat, and exp claims."""
    token = create_access_token(subject="user-123", role="user")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload
    assert payload["exp"] > payload["iat"]


def test_jwt_rejects_expired_token() -> None:
    """decode_access_token must raise InvalidTokenError when token has expired."""
    token = create_access_token(
        subject="user-123",
        role="user",
        expires_delta=timedelta(seconds=-10),
    )
    with pytest.raises(InvalidTokenError, match="Invalid or expired token"):
        decode_access_token(token)


def test_jwt_rejects_tampered_signature() -> None:
    """decode_access_token must raise InvalidTokenError on tampered signature."""
    token = create_access_token(subject="user-123", role="user")
    header, payload, signature = token.split(".")
    tampered_token = f"{header}.{payload}.{signature[:-4]}xxxx"
    with pytest.raises(InvalidTokenError):
        decode_access_token(tampered_token)


def test_jwt_rejects_malformed_token() -> None:
    """decode_access_token must raise InvalidTokenError on non-JWT strings."""
    with pytest.raises(InvalidTokenError):
        decode_access_token("this.is.not-a-valid-jwt")


def test_jwt_rejects_unsupported_algorithm() -> None:
    """decode_access_token must reject tokens signed with unsupported algorithms."""
    unsecured_token = jwt.encode(
        {"sub": "user-123", "role": "admin"},
        key="",
        algorithm="none",
    )
    with pytest.raises(InvalidTokenError):
        decode_access_token(unsecured_token)
