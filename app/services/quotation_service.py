
import logging
from datetime import date
from decimal import Decimal
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.config import BASE_DIR
from app.utilities.file_storage import (
    save_quotation_file,
)
from app.core.exceptions.exception import (
    TenderNotFoundException,
    QuotationNotFoundException,
    QuotationBusinessRuleException,
    QuotationAccessDeniedException,
)

from app.models.quotation_model import Quotation
from app.repositories.interfaces.quotation_repository_interface import (
    QuotationRepositoryInterface,
)
from app.repositories.interfaces.tender_repository_interface import (
    TenderRepositoryInterface,
)
from app.utilities.email_service import EmailService

logger = logging.getLogger(__name__)


class QuotationService:

    def __init__(
        self,
        repository: QuotationRepositoryInterface,
        tender_repository: TenderRepositoryInterface,
    ) -> None:

        self.repository = repository
        self.tender_repository = tender_repository
        self.email_service = EmailService()

    async def submit_quotation(
        self,
        tender_id: int,
        user_id: int,
        amount_quoted: Decimal,
        proposal: str,
        document: UploadFile,
    ) -> Quotation:

        vendor_id = await self.repository.get_vendor_id_by_user_id(user_id)

        if vendor_id is None:
            raise QuotationBusinessRuleException(
                "Vendor profile not found. Complete vendor registration first."
            )

        tender = await self.tender_repository.get_by_id(tender_id)

        if tender is None:
            raise TenderNotFoundException(
                f"Tender with ID {tender_id} not found."
            )

        today = date.today()

        if tender.status != "open":
            raise QuotationBusinessRuleException(
                "This tender is not accepting quotations as it is not open now."
            )

        if tender.publish_date > today:
            raise QuotationBusinessRuleException(
                "This tender has not been published yet."
            )

        if tender.end_date < today:
            raise QuotationBusinessRuleException(
                "The quotation submission deadline has passed."
            )

        if amount_quoted <= Decimal("0"):
            raise QuotationBusinessRuleException(
                "Quoted amount must be greater than zero."
            )

        existing_quotation = (
            await self.repository.get_by_tender_vendor(
                tender_id,
                vendor_id,
            )
        )

        if existing_quotation is not None:
            raise QuotationBusinessRuleException(
                "You have already submitted a quotation for this tender."
            )

        document_path = None

        try:
            document_path, original_filename = (
                await save_quotation_file(document)
            )

            quotation_data = {
                "tender_id": tender_id,
                "vendor_id": vendor_id,
                "amount_quoted": amount_quoted,
                "proposal": proposal,
                "document_path": document_path,
                "original_filename": original_filename,
                "status": "submitted",
            }

            quotation = await self.repository.create(
                quotation_data
            )

            await self.repository.commit()

            # Added email service 
            await self.email_service.send_quotation_notification_async(
                quotation_id=quotation.quotation_id,
                tender_id=quotation.tender_id,
                vendor_id=quotation.vendor_id,
                amount_quoted=str(quotation.amount_quoted),
            )

            logger.info(
                "Quotation submitted successfully. "
                "quotation_id=%s tender_id=%s vendor_id=%s",
                quotation.quotation_id,
                tender_id,
                vendor_id,
            )

            return quotation

        except ValueError as error:
            raise QuotationBusinessRuleException(
                str(error)
            ) from error

        except IntegrityError as error:
            await self.repository.rollback()

            logger.exception(
                "Database constraint error while submitting quotation. "
                "tender_id=%s vendor_id=%s",
                tender_id,
                vendor_id,
            )

            raise QuotationBusinessRuleException(
                "Unable to submit quotation. Check the tender and vendor details."
            ) from error

        except SQLAlchemyError as error:
            await self.repository.rollback()

            logger.exception(
                "Database error while submitting quotation. tender_id=%s",
                tender_id,
            )

            raise QuotationBusinessRuleException(
                "A database error occurred while submitting the quotation."
            ) from error

    async def get_quotation(
        self,
        quotation_id: int,
        user_id: int,
        role: str,
    ) -> Quotation:

        quotation = await self.repository.get_by_id(
            quotation_id
        )

        if quotation is None:
            raise QuotationNotFoundException(
                f"Quotation with ID {quotation_id} not found."
            )

        if role == "vendor":
            vendor_id = (
                await self.repository.get_vendor_id_by_user_id(
                    user_id
                )
            )

            if vendor_id is None or quotation.vendor_id != vendor_id:
                raise QuotationAccessDeniedException(
                    "You cannot access another vendor's quotation."
                )

        logger.info(
            "Quotation retrieved. quotation_id=%s user_id=%s",
            quotation_id,
            user_id,
        )

        return quotation

    async def get_my_quotations(
        self,
        user_id: int,
        page: int,
        limit: int,
    ) -> list[Quotation]:

        vendor_id = await self.repository.get_vendor_id_by_user_id(
            user_id
        )

        if vendor_id is None:
            raise QuotationBusinessRuleException(
                "Vendor profile not found."
            )

        skip = (page - 1) * limit

        return await self.repository.get_by_vendor(
            vendor_id,
            skip,
            limit,
        )

    async def get_all_quotations(
        self,
        page: int,
        limit: int,
        status: str | None = None,
    ) -> list[Quotation]:

        skip = (page - 1) * limit
        return await self.repository.get_all(
            skip,
            limit,
            status,
        )

    
    async def withdraw_quotation(
        self,
        quotation_id: int,
        user_id: int,
    ) -> Quotation:

        # Get vendor ID using authenticated user ID
        vendor_id = await self.repository.get_vendor_id_by_user_id(
            user_id
        )

        if vendor_id is None:
            raise QuotationBusinessRuleException(
                "Vendor profile not found."
            )

        # Find quotation
        quotation = await self.repository.get_by_id(
            quotation_id
        )

        if quotation is None:
            raise QuotationNotFoundException(
                f"Quotation with ID {quotation_id} not found."
            )

        # Verify ownership
        if quotation.vendor_id != vendor_id:
            raise QuotationAccessDeniedException(
                "You cannot withdraw another vendor's quotation."
            )

        # Only submitted quotations can be withdrawn
        if quotation.status != "submitted":
            raise QuotationBusinessRuleException(
                "Only submitted quotations can be withdrawn."
            )

        try:

            quotation.status = "withdrawn"

            await self.repository.commit()

            logger.info(
                "Quotation withdrawn successfully. "
                "quotation_id=%s vendor_id=%s user_id=%s",
                quotation_id,
                vendor_id,
                user_id,
            )

            return quotation

        except SQLAlchemyError as error:

            await self.repository.rollback()

            logger.exception(
                "Database error while withdrawing quotation. "
                "quotation_id=%s",
                quotation_id,
            )

            raise QuotationBusinessRuleException(
                "Unable to withdraw quotation due to a database error."
            ) from error
