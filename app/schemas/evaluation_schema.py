from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime
from decimal import Decimal
from typing import Literal


class EvaluationCreate(BaseModel):
    eligibility_score : Decimal = Field(ge=0, le=30)

    company_profile_score : Decimal = Field(ge=0, le=30)

    proposal_score : Decimal = Field(ge=0 , le=40)

    eligibility_status : Literal[
        "eligible",
        "not_eligible",
    ]

    decision: Literal[
        "approved",
        "rejected"
    ]

    remarks : str|None =None


class EvaluationResponse(BaseModel):
    evaluation_id : int 
    quotation_id : int
    eligibility_score : Decimal
    company_profile_score : Decimal
    proposal_score : Decimal
    total_score : Decimal
    eligibility_status : Literal[
        "eligible",
        "not_eligible"
    ]
    decision: Literal[
        "pending",
        "approved",
        "rejected"
    ]
    remarks : str | None
    evaluated_by : int
    evaluated_date : datetime

    model_config = ConfigDict(from_attributes=True)

    
