from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TenderStatus = Literal[
    "open",
    "closed",
    "under_evaluation",
    "assigned",
    "cancelled",
]

TenderType = Literal[
    "new_project",
    "maintenance",
    "rework",
    "upgrade",
]


class TenderCreate(BaseModel):

    tender_title: str = Field(min_length=3, max_length=150)

    description: str = Field(min_length=10)

    eligibility_criteria: str = Field(min_length=5)

    estimated_cost: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2,
    )

    publish_date: date | None = None

    end_date: date

    tender_type: TenderType

    completion_period: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_tender_dates(self):

        publish_date = self.publish_date or date.today()

        if self.end_date <= publish_date:
            raise ValueError(
                "End date must be after publish date"
            )

        if self.end_date <= date.today():
            raise ValueError(
                "End date must be in the future"
            )

        return self


class TenderUpdate(BaseModel):

    tender_title: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        min_length=10,
    )

    eligibility_criteria: str | None = Field(
        default=None,
        min_length=5,
    )

    estimated_cost: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=15,
        decimal_places=2,
    )

    publish_date: date | None = None

    end_date: date | None = None

    tender_type: TenderType | None = None

    completion_period: int | None = Field(
        default=None,
        gt=0,
    )

    @model_validator(mode="after")
    def validate_update_fields(self):

        if not self.model_fields_set:
            raise ValueError(
                "At least one field must be provided"
            )

        return self


class TenderStatusUpdate(BaseModel):

    status: TenderStatus


class TenderResponse(BaseModel):

    tender_id: int
    tender_title: str
    description: str
    eligibility_criteria: str

    estimated_cost: Decimal

    publish_date: date
    end_date: date

    status: str
    tender_type: str
    completion_period: int

    created_at: datetime
    created_by: int

    model_config = ConfigDict(from_attributes=True)

    