from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db

from app.repositories.implementations.tender_repository import TenderRepository
from app.repositories.implementations.quotation_repository import QuotationRepository
from app.repositories.implementations.tender_repository import TenderRepository


from app.services.tender_service import TenderService
from app.services.quotation_service import QuotationService
from app.services.evaluation_service import EvaluationService



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

