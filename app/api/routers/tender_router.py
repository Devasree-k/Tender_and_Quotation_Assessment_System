import logging

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth_dependency import get_current_user, require_roles
from app.api.dependencies.service_dependencies import get_tender_service
from app.models.user_model import User
from app.schemas.tender_schema import (
    TenderCreate,
    TenderResponse,
    TenderStatusUpdate,
    TenderUpdate,
)
from app.services.tender_service import TenderService

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/tenders",
    tags=["Tender Management"],
)


# Admin only: create tender
@router.post(
    "/",
    response_model=TenderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
async def create_tender(
    data: TenderCreate,
    service: TenderService = Depends(get_tender_service),
    current_admin: User = Depends(get_current_user),
) -> TenderResponse:

    return await service.create_tender(
        data,
        admin_id=current_admin.user_id,
        )


# Admin and vendor: list tenders    
@router.get(
    "/",
    response_model=list[TenderResponse],
    dependencies=[Depends(require_roles("admin", "vendor"))],
)
async def list_tenders(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    tender_status: str | None = Query(default=None, alias="status"),
    tender_type: str | None = Query(default=None),
    service: TenderService = Depends(get_tender_service),
) -> list[TenderResponse]:

    return await service.get_tenders(
        page=page,
        limit=limit,
        status=tender_status,
        tender_type=tender_type,
    )


# Admin and vendor: view open tenders
@router.get(
    "/open",
    response_model=list[TenderResponse],
    dependencies=[Depends(require_roles("admin", "vendor"))],
)
async def list_open_tenders(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: TenderService = Depends(get_tender_service),
) -> list[TenderResponse]:

    return await service.get_open_tenders(
        page=page,
        limit=limit,
    )


# Admin and vendor: get tender by ID
@router.get(
    "/{tender_id}",
    response_model=TenderResponse,
    dependencies=[Depends(require_roles("admin", "vendor"))],
)
async def read_tender(
    tender_id: int,
    service: TenderService = Depends(get_tender_service),
) -> TenderResponse:

    return await service.get_tender(tender_id)


# Admin only: update tender
@router.put(
    "/{tender_id}",
    response_model=TenderResponse,
    dependencies=[Depends(require_roles("admin"))],
)
async def update_tender(
    tender_id: int,
    data: TenderUpdate,
    service: TenderService = Depends(get_tender_service),
) -> TenderResponse:

    return await service.update_tender(
        tender_id,
        data,
    )


# Admin only: change tender status
@router.patch(
    "/{tender_id}/status",
    response_model=TenderResponse,
    dependencies=[Depends(require_roles("admin"))],
)
async def change_tender_status(
    tender_id: int,
    data: TenderStatusUpdate,
    service: TenderService = Depends(get_tender_service),
) -> TenderResponse:

    return await service.update_tender_status(
        tender_id,
        data.status,
    )