from abc import ABC, abstractmethod
from typing import Any

from app.models.quotation_model import Quotation

class QuotationRepositoryInterface(ABC):

    @abstractmethod
    async def get_vendor_email_by_quotation(self, quotation_id: int) -> str | None:
        pass

    @abstractmethod
    async def create(self, quotation_data: dict[str, Any],) -> Quotation:
        pass

    @abstractmethod 
    async def get_by_id(self, quotation_id : int )-> Quotation | None:
        pass

    @abstractmethod 
    async def get_vendor_id_by_user_id(self, user_id: int )-> int | None:
        pass

    @abstractmethod
    async def get_by_tender_vendor(self, tender_id: int, vendor_id: int )-> Quotation | None:
        pass

    @abstractmethod
    async def get_by_vendor(self, vendor_if:int ,skip:int, limit: int)->list[Quotation]:
        pass

    @abstractmethod
    async def get_all(self, skip:int, limit:int, status: str|None = None)->list[Quotation]:
        pass

    @abstractmethod
    async def commit(self)->None:
        pass

    @abstractmethod 
    async def rollback(self)-> None:
        pass
    
