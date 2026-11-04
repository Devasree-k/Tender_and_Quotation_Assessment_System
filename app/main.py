import logging

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from sqlalchemy import engine

from app.core.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


from app.api.routers.auth_router import router as auth_router
from app.api.routers.health_router import router as health_router
from app.api.routers.tender_router import router as tender_router
from app.api.routers.quotation_router import router as quotation_router
from app.api.routers.evaluation_router import router as evaluation_router
from app.api.routers.sanction_router import router as sanction_router
from app.api.routers.report_router import router as report_router

from app.core.exceptions.exception_handler import register_exception_handlers
from app.middleware.observability import RequestLoggingMiddleware

# Application startup and shutdown
@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:

    logger.info("Transport Collection API starting")

    try:
        yield

    finally:
        logger.info("Transport Collection API shutting down")
        await engine.dispose()


app = FastAPI(
    title="Tender and Quotation Assessment System",
    description=(
        "Tender and Quotation Assessment System with async SQLAlchemy, "
        "JWT authentication, and role-based authorization."
    ),
    version="1.0.0",
    lifespan=lifespan,
    )

app.add_middleware(RequestLoggingMiddleware)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tender_router)
app.include_router(quotation_router)
app.include_router(evaluation_router)
app.include_router(sanction_router)
app.include_router(report_router)

register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Tender Assessment API is running"}
