
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SanctionCreate(BaseModel):

    quotation_id: int = Field(gt=0)

    amount: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2,
    )


class SanctionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    sanction_id: int
    quotation_id: int
    tender_id: int
    sanctioned_amount: Decimal
    sanctioned_date: datetime
    sanctioned_by: int
    remarks: str | None = None
