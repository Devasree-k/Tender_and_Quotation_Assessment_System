from sqlalchemy.orm import Mapped ,mapped_column, relationship
from  sqlalchemy import String, Integer, DateTime, func, CheckConstraint, Text, Numeric

from app.database.base import Base

class Tender(Base):
    __tablename__ = "tenders"

    __table_args__=(
        CheckConstraint(
            "estimated_cost > 0",
            name="check_estimation_cost"
        ),
        CheckConstraint(
            "status IN ('open', 'closed','under_evaluation', 'assigned', 'cancelled')",
            name="check_tender_status"
        ),
        CheckConstraint(
            "tender_type IN ('new_project', 'maintenance', "
            "'rework', 'upgrade')",
            name="check_tender_type"
        ),
        CheckConstraint(
            "completion_period > 0",
            name="check_completion_period"
        )
    )

    tender_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    tender_title : Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description : Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    eligibility_criteria : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    estimated_cost: Mapped[float] = mapped_column(
        Numeric(15, 2), 
        nullable=False
    )

    publish_date : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    end_date : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status : Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    tender_type: Mapped[str] = mapped_column(
        String(30), 
        nullable=False
    )

    completion_period: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships

    creator: Mapped["User"] = relationship(
        back_populates="tenders"
    )

    quotations: Mapped[list["Quotation"]] = relationship(
        back_populates="tender"
    )

