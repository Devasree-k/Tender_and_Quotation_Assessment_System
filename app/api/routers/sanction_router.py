from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from app.api.dependencies.auth_dependency import require_roles
from app.api.dependencies.service_dependencies import (
    get_sanction_service,
)

from app.models.user_model import User

from app.schemas.sanction_schema import (
    SanctionCreate,
    SanctionResponse,
)

from app.services.sanction_service import SanctionService


router = APIRouter(
    prefix="/api/sanctions",
    tags=["Sanctions"],
)


@router.post(
    "/",
    response_model=SanctionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
async def create_sanction(
    data: SanctionCreate,
    current_admin: User = Depends(require_roles("admin")),
    service: SanctionService = Depends(get_sanction_service),
) -> SanctionResponse:

    return await service.create_sanction(
        quotation_id=data.quotation_id,
        amount=data.amount,
        admin_id=current_admin.user_id,
    )


@router.get(
    "/",
    response_model=list[SanctionResponse],
    dependencies=[Depends(require_roles("admin"))],
)
async def list_sanctions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    service: SanctionService = Depends(get_sanction_service),
) -> list[SanctionResponse]:

    return await service.get_all_sanctions(
        page=page,
        limit=limit,
    )

@router.get(
    "/tender/{tender_id}",
    response_model=SanctionResponse,
    dependencies=[Depends(require_roles("admin"))],
)
async def get_sanction_by_tender(
    tender_id: int,
    service: SanctionService = Depends(get_sanction_service),
) -> SanctionResponse:

    return await service.get_sanction_by_tender(tender_id)


@router.get(
    "/{sanction_id}",
    response_model=SanctionResponse,
    dependencies=[Depends(require_roles("admin"))],
)
async def get_sanction(
    sanction_id: int,
    service: SanctionService = Depends(get_sanction_service),
) -> SanctionResponse:

    return await service.get_sanction(sanction_id)