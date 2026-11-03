
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.models.vendor_model import Vendor


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> User | None:

        query = select(User).where(
            User.username == username
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:

        query = select(User).where(
            User.user_id == user_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def create_user(self, user_data: dict) -> User:

        user = User(**user_data)

        self.db.add(user)
        await self.db.flush()

        return user

    async def create_vendor(self, vendor_data: dict) -> Vendor:

        vendor = Vendor(**vendor_data)

        self.db.add(vendor)
        await self.db.flush()

        return vendor
