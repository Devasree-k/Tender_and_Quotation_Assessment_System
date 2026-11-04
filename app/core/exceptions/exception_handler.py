from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions.exception import (
    QuotationAccessDeniedException,
    QuotationBusinessRuleException,
    QuotationNotFoundException,
    TenderBusinessRuleException,
    TenderNotFoundException,
    EvaluationNotFoundException,
    EvaluationBusinessRuleException,
    EvaluationAccessDeniedException,
    SanctionNotFoundException,
    SanctionBusinessRuleException,
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


    @app.exception_handler(QuotationBusinessRuleException)
    async def quotation_business_rule_handler(
        request: Request,
        exc: QuotationBusinessRuleException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(QuotationNotFoundException)
    async def quotation_not_found_handler(
        request: Request,
        exc: QuotationNotFoundException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(QuotationAccessDeniedException)
    async def quotation_access_denied_handler(
        request: Request,
        exc: QuotationAccessDeniedException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=403,
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


    @app.exception_handler(SanctionNotFoundException)
    async def sanction_not_found_handler(
        request: Request,
        error: SanctionNotFoundException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(error)},
        )


    @app.exception_handler(SanctionBusinessRuleException)
    async def sanction_business_rule_handler(
        request: Request,
        error: SanctionBusinessRuleException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(error)},
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        import logging
        logger = logging.getLogger("app.exceptions")
        logger.exception(
            "Unhandled exception occurred: %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected internal error occurred.",
                "request_path": request.url.path,
            },
        )


        