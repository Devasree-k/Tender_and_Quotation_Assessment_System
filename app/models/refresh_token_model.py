from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    refresh_token_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(64), 
        unique=True, 
        nullable=False, 
        index=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )

    revoked: Mapped[bool] = mapped_column(
        default=False, 
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    
    user: Mapped[User] = relationship(back_populates="refresh_tokens")
