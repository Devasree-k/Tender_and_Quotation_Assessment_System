from abc import ABC, abstractmethod
from typing import Any

from app.models.sanction_model import Sanction


class SanctionRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, sanction_data: dict[str, Any]) -> Sanction:
        pass

    @abstractmethod
    async def get_by_id(self, sanction_id: int) -> Sanction | None:
        pass

    @abstractmethod
    async def get_by_tender(self, tender_id: int) -> Sanction | None:
        pass

    @abstractmethod
    async def get_all(self, skip: int, limit: int) -> list[Sanction]:
        pass

    @abstractmethod
    async def get_quotation_details(self,quotation_id: int,) -> Any | None:
        pass

    @abstractmethod
    async def update_tender_status(self,tender_id: int,new_status: str,) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass


    