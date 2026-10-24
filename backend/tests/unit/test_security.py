"""Unit tests for password hashing and verification in core/security.py."""

from app.core.security import hash_password, verify_password


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
