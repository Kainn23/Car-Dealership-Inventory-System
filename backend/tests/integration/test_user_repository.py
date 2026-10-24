"""Integration tests for SqlAlchemyUserRepository."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import SqlAlchemyUserRepository


def test_user_repository_create_and_get_by_email(db_session: Session) -> None:
    """User repository should persist a user and retrieve it by email."""
    repo = SqlAlchemyUserRepository(db_session)
    new_user = User(
        email="john.doe@example.com",
        password_hash="mocked_argon2_hash",
        role="user",
    )
    saved = repo.create(new_user)
    assert saved.id is not None

    retrieved = repo.get_by_email("john.doe@example.com")
    assert retrieved is not None
    assert retrieved.email == "john.doe@example.com"


def test_user_repository_get_by_email_is_case_insensitive(db_session: Session) -> None:
    """get_by_email must find user regardless of uppercase or lowercase query."""
    repo = SqlAlchemyUserRepository(db_session)
    user = User(
        email="case.test@example.com",
        password_hash="mocked_argon2_hash",
        role="user",
    )
    repo.create(user)

    retrieved = repo.get_by_email("CASE.TEST@EXAMPLE.COM")
    assert retrieved is not None
    assert retrieved.email == "case.test@example.com"


def test_user_repository_enforces_unique_lowercase_email(db_session: Session) -> None:
    """Attempting to persist duplicate emails differing only by case must fail."""
    repo = SqlAlchemyUserRepository(db_session)
    user1 = User(
        email="unique@dealership.com",
        password_hash="hash1",
        role="user",
    )
    repo.create(user1)

    user2 = User(
        email="UNIQUE@DEALERSHIP.COM",
        password_hash="hash2",
        role="user",
    )
    with pytest.raises(IntegrityError):
        repo.create(user2)


def test_user_repository_get_by_id(db_session: Session) -> None:
    """get_by_id must retrieve user by primary key UUID."""
    repo = SqlAlchemyUserRepository(db_session)
    user = User(
        email="id.lookup@example.com",
        password_hash="hash_id",
        role="admin",
    )
    saved = repo.create(user)

    retrieved = repo.get_by_id(saved.id)
    assert retrieved is not None
    assert retrieved.id == saved.id
    assert retrieved.role == "admin"
