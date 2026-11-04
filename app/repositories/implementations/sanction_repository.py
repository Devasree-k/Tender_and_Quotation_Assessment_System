from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.sanction_model import Sanction
from app.models.quotation_model import Quotation
from app.models.evaluation_model import Evaluation
from app.models.vendor_model import Vendor
from app.models.user_model import User
from app.models.tender_model import Tender

from app.repositories.interfaces.sanction_repository_interface import (
    SanctionRepositoryInterface,
)


class SanctionRepository(SanctionRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        sanction_data: dict[str, Any],
    ) -> Sanction:

        sanction = Sanction(**sanction_data)

        self.db.add(sanction)

        await self.db.flush()

        return sanction

    async def get_by_id(
        self,
        sanction_id: int,
    ) -> Sanction | None:

        query = select(Sanction).where(
            Sanction.sanction_id == sanction_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_tender(
        self,
        tender_id: int,
    ) -> Sanction | None:

        query = select(Sanction).where(
            Sanction.tender_id == tender_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int,
        limit: int,
    ) -> list[Sanction]:

        query = (
            select(Sanction)
            .order_by(Sanction.sanctioned_date.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def get_quotation_details(
        self,
        quotation_id: int,
    ) -> Any | None:

        query = (
            select(Quotation)
            .where(
                Quotation.quotation_id == quotation_id
            )
            .options(
                selectinload(Quotation.tender),
                selectinload(Quotation.evaluation),
                selectinload(Quotation.vendor).selectinload(
                    Vendor.user
                ),
            )
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def update_tender_status(
        self,
        tender_id: int,
        new_status: str,
    ) -> None:

        query = (
            update(Tender)
            .where(Tender.tender_id == tender_id)
            .values(status=new_status)
        )

        await self.db.execute(query)

        await self.db.flush()

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()