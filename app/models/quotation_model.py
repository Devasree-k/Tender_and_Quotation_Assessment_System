from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Quotation(Base):

    __tablename__ = "quotations"

    __table_args__ = (
        UniqueConstraint(
            "tender_id", "vendor_id",
            name="unique_vendor_tender_quotation"
        ),
        CheckConstraint(
            "amount_quoted > 0",
            name="check_amount_quoted"
        ),
        CheckConstraint(
            "status IN ('submitted', 'under_review', 'approved', 'rejected', 'withdrawn')",
            name="check_quotation_status"
        ),
    )

    quotation_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.tender_id"), 
        nullable=False
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.vendor_id"), 
        nullable=False
    )

    amount_quoted: Mapped[float] = mapped_column(
        Numeric(15, 2), 
        nullable=False
    )

    proposal: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )

    document_path: Mapped[str] = mapped_column(
        String(500), 
        nullable=False
    )

    original_filename: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    submitted_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20), default="submitted", nullable=False
    )

    # Relationships

    tender: Mapped[Tender] = relationship(
        back_populates="quotations"
    )

    vendor: Mapped[Vendor] = relationship(
        back_populates="quotations"
    )

    evaluation: Mapped[Evaluation | None] = relationship(
        back_populates="quotation",
        cascade="all, delete-orphan"
    )

    sanction: Mapped[Sanction | None] = relationship(
        back_populates="quotation",
        cascade="all, delete-orphan"
    )
