"""Repository protocol interfaces for dependency inversion."""

from typing import Protocol
from uuid import UUID

from app.models.user import User


class UserRepositoryProtocol(Protocol):
    """Protocol for user data persistence operations."""

    def create(self, user: User) -> User:
        """Persist a new user."""
        ...

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve user by UUID."""
        ...

    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by case-insensitive email."""
        ...
