from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db

from app.repositories.implementations.report_repository import ReportRepository
from app.repositories.implementations.tender_repository import TenderRepository
from app.repositories.implementations.quotation_repository import QuotationRepository
from app.repositories.implementations.tender_repository import TenderRepository
from app.repositories.implementations.sanction_repository import SanctionRepository

from app.services.report_service import ReportService
from app.services.tender_service import TenderService
from app.services.quotation_service import QuotationService
from app.services.evaluation_service import EvaluationService
from app.services.sanction_service import SanctionService

from app.utilities.email_service import EmailService



def get_tender_service(db: AsyncSession = Depends(get_db)) -> TenderService:
    repository = TenderRepository(db)
    return TenderService(repository)



def get_quotation_service(db: AsyncSession = Depends(get_db)) -> QuotationService:
    quotation_repository = QuotationRepository(db)
    tender_repository = TenderRepository(db)

    return QuotationService(
        repository=quotation_repository,
        tender_repository=tender_repository,
    )


async def get_evaluation_service(db: AsyncSession = Depends(get_db)) -> EvaluationService:
    return EvaluationService(db)


def get_sanction_service(db: AsyncSession = Depends(get_db)) -> SanctionService:

    repository = SanctionRepository(db)
    email_service = EmailService()

    return SanctionService(repository, email_service)



def get_report_service(db: AsyncSession = Depends(get_db),) -> ReportService:
    repository = ReportRepository(db)
    return ReportService(repository)


