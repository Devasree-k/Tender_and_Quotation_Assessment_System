from abc import ABC, abstractmethod

from typing import Any
from app.models.evaluation_model import Evaluation

class EvaluationRepositoryInterface(ABC):

    @abstractmethod
    async def create(evaluation_data : dict[str, Any])-> Evaluation:
        pass 

    @abstractmethod
    async def get_by_id(self, evaluation_id : int )->Evaluation | None:
        pass

    @abstractmethod 
    async def get_by_quotation_id(self, quotatin_id : int)-> Evaluation | None:
        pass

    @abstractmethod 
    async def get_all(self, skip:int , limit: int )->list[Evaluation]:
        pass

    @abstractmethod
    async def get_approved_by_tender(self,tender_id: int, skip: int, limit: int) -> list[Evaluation]:
        pass



