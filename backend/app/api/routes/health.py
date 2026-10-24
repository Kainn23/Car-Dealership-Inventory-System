"""Health check API route."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import check_db_health, get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(
    db: Annotated[Session, Depends(get_db)],
    response: Response,
) -> dict[str, str]:
    """Return application and database health status."""
    is_db_alive = check_db_health(db)
    if not is_db_alive:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "disconnected"}

    return {"status": "ok", "database": "connected"}
