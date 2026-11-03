
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Vendor(Base):

    __tablename__ = "vendors"

    __table_args__ = (
        CheckConstraint(
            "company_experience >= 0",
            name="check_company_experience"
        ),
        CheckConstraint(
            "company_category IN ('startup', 'medium-sized(SME)', 'large-Corporation')",
            name="check_company_stage"
        ),
    )

    vendor_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    company_name: Mapped[str] = mapped_column(
        String(200), 
        nullable=False
    )

    owner_name: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
    )

    company_phone: Mapped[str] = mapped_column(
        String(15), 
        nullable=False
    )

    pro_name: Mapped[str | None] = mapped_column(
        String(150), 
        nullable=True
    )

    pro_phone: Mapped[str | None] = mapped_column(
        String(15), 
        nullable=True
    )

    registration_id: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False
    )

    company_experience: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False
    )

    company_category: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    company_address: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )

    # Relationships

    user: Mapped[User] = relationship(
        back_populates="vendor"
    )

    quotations: Mapped[list[Quotation]] = relationship(
        back_populates="vendor"
    )

