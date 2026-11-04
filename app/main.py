import logging

from fastapi import FastAPI

from app.core.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


from app.api.routers.auth_router import router as auth_router
from app.api.routers.health_router import router as health_router
from app.api.routers.tender_router import router as tender_router
from app.api.routers.quotation_router import router as quotation_router
from app.api.routers.evaluation_router import router as evaluation_router

from app.core.exceptions.exception_handler import register_exception_handlers
from app.middleware.observability import RequestLoggingMiddleware

app = FastAPI(title="Tender and Quotation Assessment System")

app.add_middleware(RequestLoggingMiddleware)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tender_router)
app.include_router(quotation_router)
app.include_router(evaluation_router)

register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Tender Assessment API is running"}
