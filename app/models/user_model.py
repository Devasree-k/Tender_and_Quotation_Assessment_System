from sqlalchemy import Boolean, DateTime, Integer , String, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.base import Base

class User(Base):
    __tablename__="users"

    __table_args__= (
        CheckConstraint(
            "role IN ('admin','vendor')",
            name="check_user_role"
        ),
    )


    user_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username : Mapped[str] = mapped_column(
        String(50),
        nullable=False,

    )
    email : Mapped[str] = mapped_column(
        String(50),
        unique= True,
        nullable=False,
        index=True
    )

    hashed_password : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role : Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    is_active : Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships

    vendor: Mapped["Vendor | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    tenders: Mapped[list["Tender"]] = relationship(
        back_populates="creator"
    )

    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="evaluator"
    )
