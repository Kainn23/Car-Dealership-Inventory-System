"""Integration tests for the health check endpoint."""

from collections.abc import Generator
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app

client = TestClient(app)


def test_health_reports_database_status_connected() -> None:
    """GET /health should return 200 with database connected when DB is reachable."""
    mock_db = MagicMock()
    mock_db.execute.return_value = None

    def override_get_db() -> Generator[MagicMock, None, None]:
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok", "database": "connected"}
    finally:
        app.dependency_overrides.clear()


def test_health_returns_503_when_database_unreachable() -> None:
    """GET /health should return 503 when the database check fails."""
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("DB connection timeout")

    def override_get_db() -> Generator[MagicMock, None, None]:
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/health")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json() == {"status": "error", "database": "disconnected"}
    finally:
        app.dependency_overrides.clear()
