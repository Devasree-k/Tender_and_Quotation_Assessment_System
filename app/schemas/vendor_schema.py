
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.user_schema import UserCreate


class VendorCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=150)
    owner_name: str
    company_phone: str
    pro_name: str
    pro_phone: str
    registration_id: str
    company_experience: int = Field(ge=0)
    company_category: str 
    company_address: str


class VendorResponse(VendorCreate):
    vendor_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class VendorRegistration(BaseModel):
    user: UserCreate
    vendor: VendorCreate
