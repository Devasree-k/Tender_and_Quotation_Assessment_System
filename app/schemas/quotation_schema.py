from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

QuotationStatus = Literal[
    "submitted",
    "under_review",
    "approved",
    "rejected",
    "withdrawn",
]

class QuotationResponse(BaseModel):
    quotation_id : int
    tender_id : int
    vendor_id : int
    amount_quoted : Decimal
    proposal : str
    original_filename : str
    submitted_date : datetime
    status : QuotationStatus

    model_config = ConfigDict(from_attributes= True)

