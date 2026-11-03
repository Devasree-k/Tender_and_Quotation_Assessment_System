import logging
from datetime import date
from typing import Any

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.exceptions.exception import (
    InvalidTenderStatusException,
    TenderBusinessRuleException,
    TenderNotFoundException,
)
from app.models.tender_model import Tender
from app.repositories.interfaces.tender_repository_interface import (
    TenderRepositoryInterface,
)
from app.schemas.tender_schema import TenderCreate, TenderUpdate

logger = logging.getLogger(__name__)


class TenderService:

    ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
        "open": {"closed", "cancelled"},
        "closed": {"under_evaluation", "cancelled"},
        "under_evaluation": {"assigned", "closed", "cancelled"},
        "assigned": set(),
        "cancelled": set(),
    }

    def __init__(
        self,
        repository: TenderRepositoryInterface,
    ) -> None:
        self.repository = repository

    def validate_dates(
        self,
        publish_date: date,
        end_date: date,
    ) -> None:

        if end_date <= publish_date:
            raise TenderBusinessRuleException(
                "Tender end date must be after publish date."
            )

    async def create_tender(
        self,
        data: TenderCreate,
        admin_id: int,
    ) -> Tender:

        tender_data: dict[str, Any] = data.model_dump()
        publish_date: date = (
            tender_data.get("publish_date") or date.today()
        )
        end_date: date = tender_data["end_date"]
        self.validate_dates(publish_date, end_date)

        if end_date <= date.today():
            raise TenderBusinessRuleException(
                "Tender end date must be in the future."
            )

        tender_data["publish_date"] = publish_date
        tender_data["created_by"] = admin_id
        tender_data["status"] = "open"

        try:
            tender = await self.repository.create(tender_data)
            await self.repository.commit()
            logger.info(
                "Tender created successfully. tender_id=%s admin_id=%s",
                tender.tender_id,
                admin_id,
            )
            return tender

        except IntegrityError as error:
            await self.repository.rollback()

            logger.exception(
                "Database constraint error while creating tender. admin_id=%s",
                admin_id,
            )

            raise TenderBusinessRuleException(
                "Unable to create tender due to a database constraint."
            ) from error

        except SQLAlchemyError as error:
            await self.repository.rollback()

            logger.exception(
                "Database error while creating tender. admin_id=%s",
                admin_id,
            )

            raise TenderBusinessRuleException(
                "A database error occurred while creating the tender."
            ) from error


    async def get_tender(self, tender_id: int) -> Tender:

        tender = await self.repository.get_by_id(tender_id)

        if tender is None:
            logger.warning(
                "Tender not found. tender_id=%s",
                tender_id,
            )

            raise TenderNotFoundException(
                f"Tender with ID {tender_id} not found."
            )

        return tender

    async def get_tenders(
        self,
        page: int,
        limit: int,
        status: str | None = None,
        tender_type: str | None = None,
    ) -> list[Tender]:

        skip: int = (page - 1) * limit

        return await self.repository.get_all(
            skip=skip,
            limit=limit,
            status=status,
            tender_type=tender_type,
        )

    async def get_open_tenders(
        self,
        page: int,
        limit: int,
    ) -> list[Tender]:

        skip: int = (page - 1) * limit

        return await self.repository.get_open_tenders(
            skip=skip,
            limit=limit,
        )

    async def update_tender(
        self,
        tender_id: int,
        update_data: TenderUpdate,
    ) -> Tender:

        tender = await self.get_tender(tender_id)
        if tender.status != "open":
            raise TenderBusinessRuleException(
                "Only open tenders can be edited."
            )
        data: dict[str, Any] = update_data.model_dump(
            exclude_unset=True
        )

        if not data:
            raise TenderBusinessRuleException(
                "At least one field must be provided."
            )

        publish_date: date = data.get(
            "publish_date",
            tender.publish_date,
        )

        end_date: date = data.get(
            "end_date",
            tender.end_date,
        )

        self.validate_dates(publish_date, end_date)

        if end_date <= date.today():
            raise TenderBusinessRuleException(
                "Tender end date must be in the future."
            )

        try:
            updated_tender = await self.repository.update(
                tender,
                data,
            )

            await self.repository.commit()
            logger.info(
                "Tender updated successfully. tender_id=%s",
                tender_id,
            )
            return updated_tender

        except IntegrityError as error:
            await self.repository.rollback()
            logger.exception(
                "Database constraint error while updating tender. "
                "tender_id=%s",
                tender_id,
            )

            raise TenderBusinessRuleException(
                "Unable to update tender because of a database constraint."
            ) from error

        except SQLAlchemyError as error:
            await self.repository.rollback()

            logger.exception(
                "Database error while updating tender. tender_id=%s",
                tender_id,
            )

            raise TenderBusinessRuleException(
                "A database error occurred while updating the tender."
            ) from error

    async def update_tender_status(
        self,
        tender_id: int,
        new_status: str,
    ) -> Tender:

        tender = await self.get_tender(tender_id)
        current_status: str = tender.status
        allowed_statuses: set[str] = (
            self.ALLOWED_STATUS_TRANSITIONS.get(
                current_status,
                set(),
            )
        )

        if new_status not in allowed_statuses:
            logger.warning(
                "Invalid tender status transition. tender_id=%s "
                "current_status=%s requested_status=%s",
                tender_id,
                current_status,
                new_status,
            )

            raise InvalidTenderStatusException(
                f"Cannot change tender status from "
                f"'{current_status}' to '{new_status}'."
            )

        if new_status == "under_evaluation":
            if tender.end_date >= date.today():
                raise TenderBusinessRuleException(
                    "Tender cannot enter evaluation before its "
                    "closing date has passed."
                )

        try:
            updated_tender = await self.repository.update(
                tender,
                {"status": new_status},
            )

            await self.repository.commit()

            logger.info(
                "Tender status changed. tender_id=%s "
                "old_status=%s new_status=%s",
                tender_id,
                current_status,
                new_status,
            )

            return updated_tender

        except IntegrityError as error:
            await self.repository.rollback()

            logger.exception(
                "Database constraint error while changing tender status. "
                "tender_id=%s",
                tender_id,
            )

            raise TenderBusinessRuleException(
                "Unable to update tender status due to a database constraint."
            ) from error

        except SQLAlchemyError as error:
            await self.repository.rollback()

            logger.exception(
                "Database error while changing tender status. "
                "tender_id=%s",
                tender_id,
            )

            raise TenderBusinessRuleException(
                "A database error occurred while updating tender status."
            ) from error


        