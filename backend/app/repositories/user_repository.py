"""SQLAlchemy implementation of the UserRepositoryProtocol."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User


class SqlAlchemyUserRepository:
    """User repository implementation using SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: User) -> User:
        """Persist a new user into the database."""
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve user by UUID primary key."""
        statement = select(User).where(User.id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by case-insensitive email comparison."""
        statement = select(User).where(func.lower(User.email) == email.lower())
        return self.db.execute(statement).scalar_one_or_none()
