
import logging
from decimal import Decimal

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Query,
    UploadFile,
    status,
)

from app.api.dependencies.auth_dependency import require_roles
from app.api.dependencies.service_dependencies import (
    get_quotation_service,
)

from app.models.user_model import User
from app.schemas.quotation_schema import QuotationResponse
from app.services.quotation_service import QuotationService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/quotations",
    tags=["Quotations"],
)


# 1. SUBMIT QUOTATION - VENDOR

@router.post(
    "/",
    response_model=QuotationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_quotation(
    tender_id: int = Form(...),
    amount_quoted: Decimal = Form(..., gt=0),
    proposal: str = Form(..., min_length=10),
    document: UploadFile = File(...),
    current_vendor: User = Depends(require_roles("vendor")),
    service: QuotationService = Depends(get_quotation_service),
) -> QuotationResponse:

    return await service.submit_quotation(
        tender_id=tender_id,
        user_id=current_vendor.user_id,
        amount_quoted=amount_quoted,
        proposal=proposal,
        document=document,
    )


# 2. GET MY QUOTATIONS - VENDOR

@router.get(
    "/my",
    response_model=list[QuotationResponse],
    dependencies=[Depends(require_roles("vendor"))],
)
async def get_my_quotations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_vendor: User = Depends(require_roles("vendor")),
    service: QuotationService = Depends(get_quotation_service),
) -> list[QuotationResponse]:

    return await service.get_my_quotations(
        user_id=current_vendor.user_id,
        page=page,
        limit=limit,
    )


# 3. GET ALL QUOTATIONS - ADMIN

@router.get(
    "/",
    response_model=list[QuotationResponse],
    dependencies=[Depends(require_roles("admin"))],
)
async def get_all_quotations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    quotation_status: str | None = Query(
        None,
        alias="status",
    ),
    service: QuotationService = Depends(get_quotation_service),
) -> list[QuotationResponse]:

    return await service.get_all_quotations(
        page=page,
        limit=limit,
        status=quotation_status,
    )


# 4. GET QUOTATION BY ID - ADMIN / VENDOR

@router.get(
    "/{quotation_id}",
    response_model=QuotationResponse,
)
async def get_quotation(
    quotation_id: int,
    current_user: User = Depends(
        require_roles("admin", "vendor")
    ),
    service: QuotationService = Depends(get_quotation_service),
) -> QuotationResponse:

    return await service.get_quotation(
        quotation_id=quotation_id,
        user_id=current_user.user_id,
        role=current_user.role,
    )


# 5. WITHDRAW QUOTATION - VENDOR

@router.patch(
    "/{quotation_id}/withdraw",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("vendor"))],
)
async def withdraw_quotation(
    quotation_id: int,
    current_vendor: User = Depends(require_roles("vendor")),
    service: QuotationService = Depends(get_quotation_service),
) -> dict[str, str]:

    await service.withdraw_quotation(
        quotation_id=quotation_id,
        user_id=current_vendor.user_id,
    )

    logger.info(
        "Quotation withdrawal endpoint completed. "
        "quotation_id=%s user_id=%s",
        quotation_id,
        current_vendor.user_id,
    )

    return {
        "message": "Quotation withdrawn successfully.",
        "status": "withdrawn",
    }
