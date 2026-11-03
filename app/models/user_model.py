
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'vendor')",
            name="check_user_role",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="vendor",
        server_default="vendor",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    vendor: Mapped[Vendor | None] = relationship(
        "Vendor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    tenders: Mapped[list[Tender]] = relationship(
        "Tender",
        back_populates="creator",
    )

    evaluations: Mapped[list[Evaluation]] = relationship(
        "Evaluation",
        back_populates="evaluator",
    )

    sanctions: Mapped[list[Sanction]] = relationship(
        "Sanction",
        back_populates="approver"
    )

    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    
