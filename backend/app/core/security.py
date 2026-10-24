from datetime import timedelta
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2 with automatic unique salting."""
    return _password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2 hash.

    Safely catches expected verification and malformed-hash exceptions,
    returning False without masking unexpected programming errors.
    """
    try:
        return _password_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def create_access_token(
    subject: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Stub raises NotImplementedError for TDD Red phase.
    """
    raise NotImplementedError("create_access_token is not implemented yet")


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token.

    Stub raises NotImplementedError for TDD Red phase.
    """
    raise NotImplementedError("decode_access_token is not implemented yet")
