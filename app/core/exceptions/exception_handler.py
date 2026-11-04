from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.exception import (
    TenderBusinessRuleException,
    TenderNotFoundException,
    EvaluationNotFoundException,
    EvaluationBusinessRuleException,
    EvaluationAccessDeniedException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(TenderNotFoundException)
    async def tender_not_found_handler(
        request: Request,
        exc: TenderNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TenderBusinessRuleException)
    async def tender_business_rule_handler(
        request: Request,
        exc: TenderBusinessRuleException,
    ):
        return JSONResponse(
            status_code=400, 
            content={"detail": str(exc)},
        )


    @app.exception_handler(EvaluationNotFoundException)
    async def evaluation_not_found_handler(request, exc):

        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )


    @app.exception_handler(EvaluationBusinessRuleException)
    async def evaluation_business_rule_handler(request, exc):

        return JSONResponse(
            status_code=400,
            content={"detail": exc.message}
        )


    @app.exception_handler(EvaluationAccessDeniedException)
    async def evaluation_access_denied_handler(request, exc):

        return JSONResponse(
            status_code=403,
            content={"detail": exc.message}
        )


        