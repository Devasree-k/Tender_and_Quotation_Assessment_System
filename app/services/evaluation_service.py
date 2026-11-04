import logging
from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluation_model import Evaluation

from app.repositories.implementations.evaluation_repository import EvaluationRepository

from app.repositories.implementations.quotation_repository import QuotationRepository

from app.repositories.implementations.tender_repository import TenderRepository

from app.schemas.evaluation_schema import EvaluationCreate

from app.core.exceptions.exception import (
    EvaluationNotFoundException,
    EvaluationBusinessRuleException,
    QuotationNotFoundException,
    TenderNotFoundException,
)

from app.utilities.email_service import EmailService


logger = logging.getLogger(__name__)

class EvaluationService:

    def __init__(self, db: AsyncSession):

        self.db = db
        self.evaluation_repository = EvaluationRepository(db)
        self.quotation_repository = QuotationRepository(db)
        self.tender_repository = TenderRepository(db)
        self.email_service = EmailService()

    async def create_evaluation(
        self,
        quotation_id: int,
        evaluation_data: EvaluationCreate,
        admin_id: int,
    ) -> Evaluation:

        quotation = await self.quotation_repository.get_by_id(quotation_id)

        if quotation is None:
            raise QuotationNotFoundException("Quotation not found")

        tender = await self.tender_repository.get_by_id(quotation.tender_id)

        if tender is None:
            raise TenderNotFoundException("Tender not found")

        if tender.status not in [
            "closed",
            "under_evaluation",
        ]:
            raise EvaluationBusinessRuleException("Tender must be closed or under evaluation")

        existing_evaluation = (
            await self.evaluation_repository.get_by_quotation_id(
                quotation_id
            )
        )

        if existing_evaluation is not None:
            raise EvaluationBusinessRuleException(
                "This quotation has already been evaluated"
            )

        if quotation.status == "withdrawn":
            raise EvaluationBusinessRuleException(
                "Withdrawn quotations cannot be evaluated"
            )

        if (
            evaluation_data.eligibility_status == "not_eligible"
            and evaluation_data.decision == "approved"
        ):
            raise EvaluationBusinessRuleException(
                "An ineligible vendor cannot be approved"
            )

        total_score = (
            evaluation_data.eligibility_score
            + evaluation_data.company_profile_score
            + evaluation_data.proposal_score
        )

        evaluation = Evaluation(
            quotation_id=quotation_id,
            eligibility_score=evaluation_data.eligibility_score,
            company_profile_score=evaluation_data.company_profile_score,
            proposal_score=evaluation_data.proposal_score,
            total_score=total_score,
            eligibility_status=evaluation_data.eligibility_status,
            decision=evaluation_data.decision,
            remarks=evaluation_data.remarks,
            evaluated_by=admin_id,
            evaluated_date=datetime.now(timezone.utc),
        )

        try:

            await self.evaluation_repository.create(
                evaluation
            )

            quotation.status = evaluation_data.decision
            await self.db.commit()

            await self.db.refresh(evaluation)

            logger.info(
                "Quotation %s evaluated by admin %s. Total score: %s",
                quotation_id,
                admin_id,
                total_score,
            )

            vendor_email = (
                await self.quotation_repository
                .get_vendor_email_by_quotation(quotation_id)
            )

            if vendor_email:
                await self.email_service.send_evaluation_notification_async(
                    vendor_email=vendor_email,
                    quotation_id=quotation_id,
                    total_score=evaluation.total_score,
                    decision=evaluation.decision,
                    remarks=evaluation.remarks,
                )

            return evaluation

        

        except IntegrityError as exc:
            await self.db.rollback()
            logger.exception(
                "Database integrity error while evaluating quotation %s",
                quotation_id,
            )

            raise EvaluationBusinessRuleException(
                "This quotation has already been evaluated"
            ) from exc

        except Exception:

            await self.db.rollback()

            logger.exception(
                "Failed to evaluate quotation %s",
                quotation_id,
            )

            raise

    async def get_evaluation(self, evaluation_id: int) -> Evaluation:

        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)

        if evaluation is None:
            raise EvaluationNotFoundException("Evaluation not found")
        return evaluation

    async def get_evaluation_by_quotation(self, quotation_id: int,) -> Evaluation:

        evaluation = (
            await self.evaluation_repository.get_by_quotation_id(quotation_id)
        )

        if evaluation is None:
            raise EvaluationNotFoundException("Evaluation for this quotation not found")
        return evaluation

    async def get_all_evaluations( self,) -> list[Evaluation]:
        return await self.evaluation_repository.get_all()


    