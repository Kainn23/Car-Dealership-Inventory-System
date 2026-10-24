"""FastAPI application factory and entrypoint."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Car Dealership Inventory API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    return app


app = create_app()
