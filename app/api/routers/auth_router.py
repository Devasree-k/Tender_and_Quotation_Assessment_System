
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import get_current_user
from app.api.dependencies.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import (
    RefreshRequest,
    RefreshResponse,
    TokenResponse,
    UserResponse,
)
from app.schemas.vendor_schema import VendorRegistration
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ---------------- REGISTER ----------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    data: VendorRegistration,
    db: Annotated[AsyncSession, Depends(get_db)]
):

    service = AuthService(db)

    return await service.register(
        user_data=data.user,
        vendor_data=data.vendor
    )


# ---------------- LOGIN ----------------

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],
    db: Annotated[AsyncSession, Depends(get_db)]
):

    service = AuthService(db)

    return await service.login(
        username=form_data.username,
        password=form_data.password
    )


# ---------------- REFRESH TOKEN ----------------

@router.post(
    "/refresh",
    response_model=RefreshResponse
)
async def refresh_token(
    data: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):

    service = AuthService(db)

    return await service.refresh(
        data.refresh_token
    )


# ---------------- LOGOUT ----------------

@router.post("/logout")
async def logout(
    data: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):

    service = AuthService(db)

    await service.logout(data.refresh_token)

    return {
        "message": "Successfully logged out"
    }


# ---------------- CURRENT USER ----------------

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_my_profile(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ]
):

    return current_user
