from abc import ABC, abstractmethod
from typing import Any


class ReportRepositoryInterface(ABC):

    @abstractmethod
    async def get_dashboard_report(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_tender_report(self,tender_id: int | None = None,) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def get_evaluation_report(self,decision: str | None = None,) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def get_sanction_report(self, tender_id: int | None = None,) -> list[dict[str, Any]]:
        pass

    