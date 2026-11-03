from sqlalchemy import select 
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quotation_model import Quotation
from app.models.vendor_model import Vendor

from app.repositories.interfaces.quotation_repository_interface import QuotationRepositoryInterface


class QuotationRepository(QuotationRepositoryInterface):
    def __init__(self, db:AsyncSession)->None:
        self.db=db

    async def create(self, quotation_data : dict[str, Any],)->Quotation:
        quotation = Quotation(**quotation_data)
        self.db.add(quotation)
        await self.db.flush()
        return quotation    


    async def get_by_id(
        self,
        quotation_id: int,
    ) -> Quotation | None:

        query = select(Quotation).where(
            Quotation.quotation_id == quotation_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    
    async def get_vendor_id_by_user_id(
        self,
        user_id: int,
    ) -> int | None:

        query = select(Vendor.vendor_id).where(
            Vendor.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def get_by_tender_vendor(
        self,
        tender_id: int,
        vendor_id: int,
    ) -> Quotation | None:

        query = select(Quotation).where(
            Quotation.tender_id == tender_id,
            Quotation.vendor_id == vendor_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def get_by_vendor(
        self,
        vendor_id: int,
        skip: int,
        limit: int,
    ) -> list[Quotation]:

        query = (
            select(Quotation)
            .where(Quotation.vendor_id == vendor_id)
            .order_by(Quotation.submitted_date.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


    async def get_all(
        self,
        skip: int,
        limit: int,
        status: str | None = None,
    ) -> list[Quotation]:

        query = select(Quotation)
        if status is not None:
            query = query.where(Quotation.status == status)

        query = (
            query
            .order_by(Quotation.submitted_date.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


    async def commit(self) -> None:
        await self.db.commit()


    async def rollback(self) -> None:
        await self.db.rollback()




