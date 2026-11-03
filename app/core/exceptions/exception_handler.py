from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.exception import (
    TenderBusinessRuleException,
    TenderNotFoundException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(TenderNotFoundException)
    async def tender_not_found_handler(
        request: Request,
        exc: TenderNotFoundException,
    ):
        return JSONResponse(status_code=404,content={"detail": str(exc)},)

    @app.exception_handler(TenderBusinessRuleException)
    async def tender_business_rule_handler(
        request: Request,
        exc: TenderBusinessRuleException,
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)},)

    


    