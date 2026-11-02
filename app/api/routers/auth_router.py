
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.schemas.user_schema import UserResponse, TokenResponse
from app.schemas.vendor_schema import VendorRegistration
from app.services.auth_service import AuthService
from app.api.dependencies.auth_dependency import get_current_user
from app.models.user_model import User


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


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


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = AuthService(db)

    return await service.login(
        email=form_data.username,
        password=form_data.password
    )


@router.get(
    "/me",
    response_model=UserResponse
)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
