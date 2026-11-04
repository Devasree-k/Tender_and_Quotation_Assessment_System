import logging
from datetime import date
from decimal import Decimal

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.exceptions.exception import (
    SanctionNotFoundException,
    SanctionBusinessRuleException,
)

from app.models.sanction_model import Sanction

from app.repositories.interfaces.sanction_repository_interface import (
    SanctionRepositoryInterface,
)

from app.utilities.email_service import EmailService


logger = logging.getLogger(__name__)


class SanctionService:

    def __init__(
        self,
        repository: SanctionRepositoryInterface,
        email_service: EmailService,
    ) -> None:

        self.repository = repository
        self.email_service = email_service

    async def create_sanction(
        self,
        quotation_id: int,
        amount: Decimal,
        admin_id: int,
    ) -> Sanction:

        quotation = await self.repository.get_quotation_details(
            quotation_id
        )

        if quotation is None:
            raise SanctionNotFoundException(
                f"Quotation with ID {quotation_id} not found."
            )

        tender = quotation.tender

        if tender is None:
            raise SanctionBusinessRuleException(
                "The tender associated with this quotation was not found."
            )

        evaluation = quotation.evaluation

        if evaluation is None:
            raise SanctionBusinessRuleException(
                "This quotation has not been evaluated."
            )

        if evaluation.decision != "approved":
            raise SanctionBusinessRuleException(
                "Only approved quotations can be sanctioned."
            )

        if tender.status != "under_evaluation":
            raise SanctionBusinessRuleException(
                "Only tenders under evaluation can be sanctioned."
            )

        existing_sanction = await self.repository.get_by_tender(
            tender.tender_id
        )

        if existing_sanction is not None:
            raise SanctionBusinessRuleException(
                "This tender has already been sanctioned."
            )

        if amount <= Decimal("0"):
            raise SanctionBusinessRuleException(
                "Sanctioned amount must be greater than zero."
            )

        sanction_data = {
            "quotation_id": quotation.quotation_id,
            "tender_id": tender.tender_id,
            "sanctioned_amount" : amount,
            "sanctioned_by": admin_id,
            "remarks": None,
        }

        try:

            sanction = await self.repository.create(
                sanction_data
            )

            await self.repository.update_tender_status(
                tender.tender_id,
                "assigned",
            )

            # Save sanction and tender status together.
            await self.repository.commit()

            logger.info(
                "Tender sanctioned successfully. "
                "sanction_id=%s tender_id=%s quotation_id=%s admin_id=%s",
                sanction.sanction_id,
                tender.tender_id,
                quotation_id,
                admin_id,
            )

            # Email should be sent only after the transaction commits.
            vendor = quotation.vendor
            user = vendor.user if vendor else None

            if user and user.email:

                await self.email_service.send_award_notification_async(
                    vendor_email=user.email,
                    vendor_name=vendor.owner_name,
                    tender_title=tender.tender_title,
                    tender_id=tender.tender_id,
                    sanctioned_amount=amount,
                    sanction_date=date.today(),
                )

            else:
                logger.warning(
                    "Award email not sent because vendor email is missing. "
                    "quotation_id=%s",
                    quotation_id,
                )
            

        except IntegrityError as error:

            await self.repository.rollback()

            logger.exception(
                "Constraint violation while sanctioning tender. "
                "quotation_id=%s",
                quotation_id,
            )

            raise SanctionBusinessRuleException(
                "This tender or quotation may already have been sanctioned."
            ) from error

        except SQLAlchemyError as error:

            await self.repository.rollback()

            logger.exception(
                "Database error while sanctioning quotation_id=%s",
                quotation_id,
            )

            raise SanctionBusinessRuleException(
                "A database error occurred while creating the sanction."
            ) from error

        
        return sanction

    async def get_sanction(
        self,
        sanction_id: int,
    ) -> Sanction:

        sanction = await self.repository.get_by_id(
            sanction_id
        )

        if sanction is None:
            raise SanctionNotFoundException(
                f"Sanction with ID {sanction_id} not found."
            )

        return sanction

    async def get_sanction_by_tender(
        self,
        tender_id: int,
    ) -> Sanction:

        sanction = await self.repository.get_by_tender(
            tender_id
        )

        if sanction is None:
            raise SanctionNotFoundException(
                f"No sanction found for tender ID {tender_id}."
            )

        return sanction

    async def get_all_sanctions(
        self,
        page: int,
        limit: int,
    ) -> list[Sanction]:

        skip = (page - 1) * limit

        return await self.repository.get_all(
            skip,
            limit,
        )