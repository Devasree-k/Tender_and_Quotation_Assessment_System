from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_model import Tender
from app.repositories.interfaces.tender_repository_interface import (
    TenderRepositoryInterface,
)


class TenderRepository(TenderRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, tender_data: dict[str, Any]) -> Tender:
        tender = Tender(**tender_data)

        self.db.add(tender)
        await self.db.flush()

        return tender

    async def get_by_id(self, tender_id: int) -> Tender | None:
        query = select(Tender).where(
            Tender.tender_id == tender_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int,
        limit: int,
        status: str | None = None,
        tender_type: str | None = None,
    ) -> list[Tender]:

        query = select(Tender)

        if status is not None:
            query = query.where(Tender.status == status)

        if tender_type is not None:
            query = query.where(Tender.tender_type == tender_type)

        query = (
            query
            .order_by(Tender.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def get_open_tenders(
        self,
        skip: int,
        limit: int,
    ) -> list[Tender]:

        today: date = date.today()

        query = (
            select(Tender)
            .where(
                Tender.status == "open",
                Tender.publish_date <= today,
                Tender.end_date >= today,
            )
            .order_by(Tender.end_date.asc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def update(
        self,
        tender: Tender,
        tender_data: dict[str, Any],
    ) -> Tender:

        for key, value in tender_data.items():
            setattr(tender, key, value)

        await self.db.flush()

        return tender

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

        