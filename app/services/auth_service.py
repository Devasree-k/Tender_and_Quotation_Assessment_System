from fastapi import HTTPException , status
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.implementations.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.models.user_model import User
from app.schemas.user_schema import TokenResponse, UserCreate
from app.schemas.vendor_schema import VendorCreate

class AuthService:
    def __init__(self,db:AsyncSession):
        self.db= db
        self.repository = UserRepository(db)

    async def register(self, user_data : UserCreate , vendor_data: VendorCreate)->User:
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                details="Email already registered"
            )
        try:
            user=await self.repository.create_user({
                "username" : user_data.username,
                "email" : user_data.email,
                "hashed_password" : hash_password(user_data.password),
                "role" : "vendor",
                "is_active" : True
            })

            await self.repository.create_vendor({
                **vendor_data.model_dump(),
                "user_id" : user.user_id,
            })

            await self.db.commit()
            await self.db.refresh(user)
            return user
        
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail="Email or vendor registartion id already exists."
            )

        except Exception:
            await self.db.rollback()
            raise

    async def login(self, email:str , password:str) -> dict[str, str]:
        user = await self.repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        access_token = create_access_token(
            user_id=user.user_id,
            role=user.role
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


    async def get_user_profile(self, user_id: int)-> User:
        user = await self.repository.get_by_id(user_id)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        return user


    