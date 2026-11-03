from abc import ABC, abstractmethod


class TenderRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, tender_data: dict):
        pass

    @abstractmethod
    async def get_by_id(self, tender_id: int):
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int,
        limit: int,
        status: str | None = None,
        tender_type: str | None = None,
    ):
        pass

    @abstractmethod
    async def get_open_tenders(self, skip: int, limit: int):
        pass

    @abstractmethod
    async def update(self, tender, tender_data: dict):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass