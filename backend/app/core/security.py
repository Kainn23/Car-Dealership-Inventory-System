"""Security utilities for password hashing and authentication."""


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2.

    Stub raises NotImplementedError for TDD Red phase.
    """
    raise NotImplementedError("hash_password is not implemented yet")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2 hash.

    Stub raises NotImplementedError for TDD Red phase.
    """
    raise NotImplementedError("verify_password is not implemented yet")
