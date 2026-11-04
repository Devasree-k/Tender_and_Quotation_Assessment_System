import logging

from fastapi import APIRouter, Depends, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User

from app.schemas.evaluation_schema import (
    EvaluationCreate,
    EvaluationResponse,
)

from app.services.evaluation_service import EvaluationService

from app.api.dependencies.service_dependencies import get_evaluation_service
from app.api.dependencies.auth_dependency import require_roles
from app.core.exceptions.exception import EvaluationAccessDeniedException


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/evaluations",
    tags=["Evaluations"],
)


# Admin creates an evaluation
@router.post(
    "/{quotation_id}",
    response_model=EvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_evaluation(
    quotation_id: int,
    evaluation_data: EvaluationCreate,
    current_admin: User = Depends(
        require_roles("admin")
    ),
    service: EvaluationService = Depends(
        get_evaluation_service
    ),
):

    return await service.create_evaluation(
        quotation_id=quotation_id,
        evaluation_data=evaluation_data,
        admin_id=current_admin.user_id,
    )


# Admin gets all evaluations
@router.get(
    "/",
    response_model=list[EvaluationResponse],
    dependencies=[Depends(require_roles("admin"))],
)
async def get_all_evaluations(
    service: EvaluationService = Depends(
        get_evaluation_service
    ),
):

    return await service.get_all_evaluations()


# Get evaluation using quotation ID
@router.get(
    "/quotation/{quotation_id}",
    response_model=EvaluationResponse,
)
async def get_evaluation_by_quotation(
    quotation_id: int,
    current_user: User = Depends(
        require_roles("admin", "vendor")
    ),
    service: EvaluationService = Depends(get_evaluation_service),
):

    evaluation = await service.get_evaluation_by_quotation(quotation_id)

    if current_user.role == "vendor":

        quotation = await service.quotation_repository.get_by_id(
            quotation_id
        )

        if quotation is None:
            raise EvaluationAccessDeniedException()

        vendor = await service.quotation_repository.get_vendor_by_user_id(
            current_user.user_id
        )

        if vendor is None or quotation.vendor_id != vendor.vendor_id:
            raise EvaluationAccessDeniedException(
                "You can only view your own evaluation"
            )

    return evaluation


# Admin gets evaluation by evaluation ID
@router.get(
    "/{evaluation_id}",
    response_model=EvaluationResponse,
    dependencies=[Depends(require_roles("admin"))],
)
async def get_evaluation(
    evaluation_id: int,
    service: EvaluationService = Depends(get_evaluation_service),
):

    return await service.get_evaluation(evaluation_id)


# to retrieve the evaluation for particular tender
@router.get(
    "/approved/tender/{tender_id}",
    response_model=list[EvaluationResponse],
    dependencies=[Depends(require_roles("admin"))],
)
async def get_approved_quotations_by_tender(
    tender_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    service: EvaluationService = Depends(get_evaluation_service),
) -> list[EvaluationResponse]:

    return await service.get_approved_quotations_by_tender(
        tender_id=tender_id,
        page=page,
        limit=limit,
    )