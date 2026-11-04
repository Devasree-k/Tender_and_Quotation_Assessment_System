import logging
from typing import Any

from app.repositories.interfaces.report_repository_interface import (
    ReportRepositoryInterface,
)

logger = logging.getLogger(__name__)


class ReportService:

    def __init__(
        self,
        repository: ReportRepositoryInterface,
    ) -> None:

        self.repository = repository

    async def get_dashboard_report(self) -> dict[str, Any]:

        report = await self.repository.get_dashboard_report()

        logger.info("Dashboard report generated successfully")

        return report

    async def get_tender_report(
        self,
        tender_id: int | None = None,
    ) -> list[dict[str, Any]]:

        report = await self.repository.get_tender_report(
            tender_id
        )

        logger.info(
            "Tender report generated. tender_id=%s",
            tender_id,
        )

        return report

    async def get_evaluation_report(
        self,
        decision: str | None = None,
    ) -> list[dict[str, Any]]:

        report = await self.repository.get_evaluation_report(
            decision
        )

        logger.info(
            "Evaluation report generated. decision=%s",
            decision,
        )

        return report

    async def get_sanction_report(
        self,
        tender_id: int | None = None,
    ) -> list[dict[str, Any]]:

        report = await self.repository.get_sanction_report(
            tender_id
        )

        logger.info(
            "Sanction report generated. tender_id=%s",
            tender_id,
        )

        return report

    