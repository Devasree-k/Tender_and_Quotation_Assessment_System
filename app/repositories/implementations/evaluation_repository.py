from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluation_model import Evaluation
from app.repositories.interfaces.evaluation_repository_interface import EvaluationRepositoryInterface

class EvaluationRepository(EvaluationRepositoryInterface):
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create(self, evaluation_data: Evaluation) -> Evaluation :

        self.db.add(evaluation_data)
        await self.db.flush()
    
        return evaluation_data

    async def get_by_id(self, evaluation_id : int)-> Evaluation | None:

        result = await self.db.execute(
            select(Evaluation).where(
                Evaluation.evaluation_id ==evaluation_id )
        )
        return result.scalar_one_or_none()

    async def get_by_quotation_id(self, quotation_id: int ) -> Evaluation | None:

        result = await self.db.execute(
            select(Evaluation).where(
                Evaluation.quotation_id == quotation_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Evaluation]:

        result = await self.db.execute(
            select(Evaluation).order_by(
                Evaluation.evaluated_date.desc()
            )
        )

        return list(result.scalars().all())

