
from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Evaluation(Base):

    __tablename__ = "evaluations"

    __table_args__ = (
        CheckConstraint(
            "eligibility_score >= 0 AND eligibility_score <= 30",
            name="check_eligibility_score"
        ),
        CheckConstraint(
            "company_profile_score >= 0 "
            "AND company_profile_score <= 30",
            name="check_company_profile_score"
        ),
        CheckConstraint(
            "proposal_score >= 0 AND proposal_score <= 40",
            name="check_proposal_score"
        ),
        CheckConstraint(
            "total_score >= 0 AND total_score <= 100",
            name="check_total_score"
        ),
        CheckConstraint(
            "eligibility_status IN ('eligible', 'not_eligible')",
            name="check_eligibility_status"
        ),
        CheckConstraint(
            "decision IN ('pending', 'approved', 'rejected')",
            name="check_evaluation_decision"
        ),
    )

    evaluation_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    quotation_id: Mapped[int] = mapped_column(
        ForeignKey("quotations.quotation_id"),
        unique=True,
        nullable=False
    )

    eligibility_score: Mapped[float] = mapped_column(
        Numeric(5, 2), 
        nullable=False
    )

    company_profile_score: Mapped[float] = mapped_column(
        Numeric(5, 2), 
        nullable=False
    )

    proposal_score: Mapped[float] = mapped_column(
        Numeric(5, 2), 
        nullable=False
    )

    total_score: Mapped[float] = mapped_column(
        Numeric(5, 2), 
        nullable=False
    )

    eligibility_status: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )

    decision: Mapped[str] = mapped_column(
        String(20), 
        default="pending", 
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
    )

    evaluated_by: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), 
        nullable=False
    )

    evaluated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )

    # Relationships

    quotation: Mapped["Quotation"] = relationship(
        back_populates="evaluation"
    )

    evaluator: Mapped["User"] = relationship(
        back_populates="evaluations"
    )
