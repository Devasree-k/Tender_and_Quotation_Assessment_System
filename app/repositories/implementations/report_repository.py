import logging
from typing import Any

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_model import Tender
from app.models.quotation_model import Quotation
from app.models.evaluation_model import Evaluation
from app.models.sanction_model import Sanction
from app.models.vendor_model import Vendor
from app.models.user_model import User

from app.repositories.interfaces.report_repository_interface import (
    ReportRepositoryInterface,
)

logger = logging.getLogger(__name__)


class ReportRepository(ReportRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # REPORT 1: DASHBOARD SUMMARY
    async def get_dashboard_report(self) -> dict[str, Any]:
        try:
            tender_count = await self.db.scalar(
                select(func.count(Tender.tender_id))
            )

            open_tenders = await self.db.scalar(
                select(func.count(Tender.tender_id))
                .where(Tender.status == "open")
            )

            assigned_tenders = await self.db.scalar(
                select(func.count(Tender.tender_id))
                .where(Tender.status == "assigned")
            )

            quotation_count = await self.db.scalar(
                select(func.count(Quotation.quotation_id))
                .where(Quotation.status != "withdrawn")
            )

            withdrawn_count = await self.db.scalar(
                select(func.count(Quotation.quotation_id))
                .where(Quotation.status == "withdrawn")
            )

            evaluation_count = await self.db.scalar(
                select(func.count(Evaluation.evaluation_id))
            )

            approved_count = await self.db.scalar(
                select(func.count(Evaluation.evaluation_id))
                .where(Evaluation.decision == "approved")
            )

            rejected_count = await self.db.scalar(
                select(func.count(Evaluation.evaluation_id))
                .where(Evaluation.decision == "rejected")
            )

            sanction_count = await self.db.scalar(
                select(func.count(Sanction.sanction_id))
            )

            total_sanction_amount = await self.db.scalar(
                select(
                    func.coalesce(
                        func.sum(Sanction.sanctioned_amount),
                        0,
                    )
                )
            )

            return {
                "total_tenders": tender_count or 0,
                "open_tenders": open_tenders or 0,
                "assigned_tenders": assigned_tenders or 0,
                "total_quotations": quotation_count or 0,
                "withdrawn_quotations": withdrawn_count or 0,
                "total_evaluations": evaluation_count or 0,
                "approved_evaluations": approved_count or 0,
                "rejected_evaluations": rejected_count or 0,
                "total_sanctions": sanction_count or 0,
                "total_sanction_amount": total_sanction_amount or 0,
            }

        except Exception:
            logger.exception("Failed to generate dashboard report")
            raise

    # REPORT 2: TENDER-WISE QUOTATION REPORT
    async def get_tender_report(self, tender_id: int | None = None) -> list[dict[str, Any]]:

        try:
            query = (
                select(
                    Tender.tender_id,
                    Tender.tender_title,
                    Tender.status.label("tender_status"),

                    func.count(
                        case(
                            (
                                Quotation.status != "withdrawn",
                                Quotation.quotation_id,
                            )
                        )
                    ).label("total_quotations"),

                    func.count(
                        case(
                            (
                                Quotation.status == "withdrawn",
                                Quotation.quotation_id,
                            )
                        )
                    ).label("withdrawn_quotations"),

                    func.coalesce(
                        func.sum(
                            case(
                                (
                                    Quotation.status != "withdrawn",
                                    Quotation.amount_quoted,
                                ),
                                else_=0,
                            )
                        ),
                        0,
                    ).label("total_quoted_amount"),

                    func.avg(
                        case(
                            (
                                Quotation.status != "withdrawn",
                                Quotation.amount_quoted,
                            ),
                            else_=None,
                        )
                    ).label("average_quoted_amount"),
                )
                .outerjoin(
                    Quotation,
                    Quotation.tender_id == Tender.tender_id,
                )
            )

            if tender_id is not None:
                query = query.where(Tender.tender_id == tender_id)

            query = query.group_by(
                Tender.tender_id,
                Tender.tender_title,
                Tender.status,
            ).order_by(Tender.tender_id.desc())

            result = await self.db.execute(query)

            return [
                dict(row)
                for row in result.mappings().all()
            ]

        except Exception:
            logger.exception(
                "Failed to generate tender report. tender_id=%s",
                tender_id,
            )
            raise

    # REPORT 3: EVALUATION REPORT
    async def get_evaluation_report(self, decision: str | None = None) -> list[dict[str, Any]]:

        try:
            query = (
                select(
                    Tender.tender_id,
                    Tender.tender_title,

                    Evaluation.evaluation_id,
                    Evaluation.decision,
                    Evaluation.total_score,

                    Quotation.quotation_id,
                    Quotation.amount_quoted,
                    Quotation.status.label("quotation_status"),
                )
                .join(
                    Quotation,
                    Quotation.quotation_id
                    == Evaluation.quotation_id,
                )
                .join(
                    Tender,
                    Tender.tender_id == Quotation.tender_id,
                )
                .where(
                    Quotation.status != "withdrawn"
                )
            )

            if decision is not None:
                query = query.where(Evaluation.decision == decision)

            query = query.order_by(Evaluation.evaluation_id.desc())
            result = await self.db.execute(query)
            return [
                dict(row)
                for row in result.mappings().all()
            ]

        except Exception:
            logger.exception("Failed to generate evaluation report")
            raise

    # REPORT 4: SANCTION / AWARD REPORT
    async def get_sanction_report(self,tender_id: int | None = None) -> list[dict[str, Any]]:

        try:
            query = (
                select(
                    Sanction.sanction_id,
                    Sanction.tender_id,
                    Sanction.quotation_id,

                    Tender.tender_title,

                    Vendor.vendor_id,
                    Vendor.company_name,
                    Vendor.owner_name,

                    User.email.label("vendor_email"),

                    Quotation.amount_quoted,

                    Sanction.sanctioned_amount,
                    Sanction.sanctioned_date,
                    Sanction.sanctioned_by,
                    Sanction.remarks,
                )
                .join(
                    Tender,
                    Tender.tender_id == Sanction.tender_id,
                )
                .join(
                    Quotation,
                    Quotation.quotation_id
                    == Sanction.quotation_id,
                )
                .join(
                    Vendor,
                    Vendor.vendor_id == Quotation.vendor_id,
                )
                .join(
                    User,
                    User.user_id == Vendor.user_id,
                )
            )

            if tender_id is not None:
                query = query.where(Sanction.tender_id == tender_id)

            query = query.order_by(Sanction.sanctioned_date.desc())
            result = await self.db.execute(query)
            return [
                dict(row)
                for row in result.mappings().all()
            ]

        except Exception:
            logger.exception(
                "Failed to generate sanction report. tender_id=%s",
                tender_id,
            )
            raise

