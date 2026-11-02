from abc import ABC, abstractmethod

from app.models.user_model import User
from app.models.vendor_model import Vendor

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User|None:
        pass

    @abstractmethod 
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod 
    async def create_user(self, user_data: dict) -> User:
        pass

    @abstractmethod
    async def create_vendor(self, vendor_data: dict) -> Vendor:
        pass