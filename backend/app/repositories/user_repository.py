"""SQLAlchemy implementation of the UserRepositoryProtocol."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


class SqlAlchemyUserRepository:
    """User repository implementation using SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: User) -> User:
        """Persist a new user. Stub for TDD Red phase."""
        raise NotImplementedError("create is not implemented yet")

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve user by UUID. Stub for TDD Red phase."""
        raise NotImplementedError("get_by_id is not implemented yet")

    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email. Stub for TDD Red phase."""
        raise NotImplementedError("get_by_email is not implemented yet")
