"""Shared pytest fixtures for backend tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app

test_engine = create_engine(
    settings.TEST_DATABASE_URL,
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def setup_test_db() -> Generator[None, None, None]:
    """Create test tables once per test session if reachable, and clean up at end."""
    try:
        Base.metadata.create_all(bind=test_engine)
        yield
        Base.metadata.drop_all(bind=test_engine)
    except Exception:
        yield


@pytest.fixture
def db_session(setup_test_db: None) -> Generator[Session, None, None]:
    """Provide an isolated database session rolled back after every test."""
    try:
        connection = test_engine.connect()
        transaction = connection.begin()
        session = TestingSessionLocal(bind=connection)

        yield session

        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()
    except Exception:
        # Fallback when test DB instance is not running
        session = TestingSessionLocal()
        yield session
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
