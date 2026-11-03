
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Sanction(Base):

    __tablename__ = "sanctions"

    __table_args__ = (
        CheckConstraint(
            "sanctioned_amount > 0",
            name="check_sanctioned_amount"
        ),
    )

    sanction_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    quotation_id: Mapped[int] = mapped_column(
        ForeignKey("quotations.quotation_id"),
        unique=True,
        nullable=False
    )

    tender_id : Mapped[int] = mapped_column(
        ForeignKey("tenders.tender_id"),
        unique=True,
        nullable=False
    )

    sanctioned_amount: Mapped[float] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    sanctioned_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    sanctioned_by: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), 
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
    )

    # Relationships

    quotation: Mapped[Quotation] = relationship(
        back_populates="sanction"
    )

    approver: Mapped[User] = relationship(
        back_populates="sanctions"
    )
