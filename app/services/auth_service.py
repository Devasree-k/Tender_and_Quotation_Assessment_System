
import logging
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.models.refresh_token_model import RefreshToken
from app.models.user_model import User
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.schemas.vendor_schema import VendorCreate

logger = logging.getLogger(__name__)


class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    # REGISTER 

    async def register(
        self,
        user_data: UserCreate,
        vendor_data: VendorCreate
    ) -> User:

        existing_user = await self.repository.get_by_username(
            user_data.username
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username already registered"
            )

        try:

            user = await self.repository.create_user({
                "username": user_data.username,
                "email": str(user_data.email),
                "hashed_password": hash_password(
                    user_data.hash_password
                ),
                "role": "vendor",
                "is_active": True,
            })

            await self.repository.create_vendor({
                **vendor_data.model_dump(),
                "user_id": user.user_id
            })

            await self.db.commit()
            await self.db.refresh(user)

            logger.info(
                "Vendor registered successfully: user_id=%s",
                user.user_id
            )

            return user

        except IntegrityError as exc:

            await self.db.rollback()

            logger.warning(
                "Registration failed due to duplicate or invalid data"
            )

            raise HTTPException(
                status_code=409,
                detail="Username, email or vendor registration ID already exists"
            ) from exc

        except Exception:

            await self.db.rollback()

            logger.exception("Registration failed")

            raise

    #LOGIN 
    async def login(self, username: str, password: str) -> dict[str, str]:

        user = await self.repository.get_by_username(username)

        if not user:

            logger.warning(
                "Login failed: username not found"
            )

            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not verify_password(password, user.hashed_password):
            logger.warning(
                "Login failed: incorrect password for user_id=%s",
                user.user_id
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="Account is inactive"
            )

        access_token = create_access_token(user.user_id,user.role)
        refresh_token = create_refresh_token()
        self.db.add(
            RefreshToken(
                user_id=user.user_id,
                token_hash=hash_refresh_token(refresh_token),
                expires_at=datetime.now(UTC) + timedelta(
                    days=REFRESH_TOKEN_EXPIRE_DAYS
                )
            )
        )

        await self.db.commit()

        logger.info(
            "User logged in successfully: user_id=%s",
            user.user_id
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    # REFRESH TOKEN 

    async def refresh(
        self,
        refresh_token: str
    ) -> dict[str, str]:

        token_hash = hash_refresh_token(refresh_token)

        record = await self.db.scalar(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )

        now = datetime.now(UTC)

        if not record:

            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        expiry = record.expires_at

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=UTC)

        if record.revoked or expiry <= now:

            raise HTTPException(
                status_code=401,
                detail="Refresh token expired or revoked"
            )

        user = await self.repository.get_by_id(record.user_id)

        if not user or not user.is_active:

            raise HTTPException(
                status_code=401,
                detail="User is inactive or unavailable"
            )

        # Revoke the old refresh token
        record.revoked = True

        # Generate new tokens
        new_refresh_token = create_refresh_token()

        self.db.add(
            RefreshToken(
                user_id=user.user_id,
                token_hash=hash_refresh_token(new_refresh_token),
                expires_at=now + timedelta(
                    days=REFRESH_TOKEN_EXPIRE_DAYS
                )
            )
        )

        await self.db.commit()

        logger.info(
            "Refresh token rotated: user_id=%s",
            user.user_id
        )

        return {
            "access_token": create_access_token(
                user.user_id,
                user.role
            ),
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    # LOGOUT

    async def logout(self, refresh_token: str) -> None:
        record = await self.db.scalar(
            select(RefreshToken).where(
                RefreshToken.token_hash ==
                hash_refresh_token(refresh_token)
            )
        )

        if record and not record.revoked:
            record.revoked = True
            await self.db.commit()
            logger.info(
                "User logged out: user_id=%s",
                record.user_id
            )

    #  USER PROFILE

    async def get_user_profile(self,user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="User not found or inactive"
            )

        return user
