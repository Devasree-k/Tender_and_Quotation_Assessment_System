from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Tender(Base):

    __tablename__ = "tenders"

    __table_args__ = (
        CheckConstraint(
            "estimated_cost > 0",
            name="check_estimation_cost",
        ),
        CheckConstraint(
            "status IN ('open', 'closed', 'under_evaluation', 'assigned', 'cancelled')",
            name="check_tender_status",
        ),
        CheckConstraint(
            "tender_type IN ('new_project', 'maintenance', 'rework', 'upgrade')",
            name="check_tender_type",
        ),
        CheckConstraint(
            "completion_period > 0",
            name="check_completion_period",
        ),
        CheckConstraint(
            "end_date > publish_date",
            name="check_tender_dates",
        ),
    )

    tender_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tender_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    eligibility_criteria: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    publish_date: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date(),
    )

    end_date: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="open",
        server_default="open",
    )

    tender_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    completion_period: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False,
    )

    # Relationships

    creator: Mapped[User] = relationship(
        back_populates="tenders",
    )

    quotations: Mapped[list[Quotation]] = relationship(
        back_populates="tender",
    )