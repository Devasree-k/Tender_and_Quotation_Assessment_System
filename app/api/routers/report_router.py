import logging

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from app.api.dependencies.auth_dependency import require_roles

from app.api.dependencies.service_dependencies import (
    get_report_service,
)

from app.services.report_service import ReportService


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


# -------------------------------------------------
# REPORT 1: DASHBOARD REPORT
# -------------------------------------------------

@router.get(
    "/dashboard",
    dependencies=[Depends(require_roles("admin"))],
)
async def dashboard_report(
    service: ReportService = Depends(get_report_service),
):

    return await service.get_dashboard_report()


# -------------------------------------------------
# REPORT 2: TENDER-WISE REPORT
# -------------------------------------------------

@router.get(
    "/tenders",
    dependencies=[Depends(require_roles("admin"))],
)
async def tender_report(
    tender_id: int | None = Query(None, gt=0),
    service: ReportService = Depends(get_report_service),
):

    return await service.get_tender_report(
        tender_id=tender_id,
    )


# -------------------------------------------------
# REPORT 3: EVALUATION REPORT
# -------------------------------------------------

@router.get(
    "/evaluations",
    dependencies=[Depends(require_roles("admin"))],
)
async def evaluation_report(
    decision: str | None = Query(
        None,
        pattern="^(approved|rejected|pending)$",
    ),
    service: ReportService = Depends(get_report_service),
):

    return await service.get_evaluation_report(
        decision=decision,
    )


# -------------------------------------------------
# REPORT 4: SANCTION / AWARD REPORT
# -------------------------------------------------

@router.get(
    "/sanctions",
    dependencies=[Depends(require_roles("admin"))],
)
async def sanction_report(
    tender_id: int | None = Query(None, gt=0),
    service: ReportService = Depends(get_report_service),
):

    return await service.get_sanction_report(
        tender_id=tender_id,
    )