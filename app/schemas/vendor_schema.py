from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user_schema import UserCreate


class VendorCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=200)
    owner_name: str = Field(min_length=2, max_length=150)
    company_phone: str = Field(min_length=7, max_length=15)
    pro_name: str | None = Field(default=None, max_length=150)
    pro_phone: str | None = Field(default=None, max_length=15)
    registration_id: str = Field(min_length=2, max_length=100)
    company_experience: int = Field(ge=0, le=100)
    company_category: str
    company_address: str

class VendorResponse(VendorCreate):
    vendor_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class VendorRegistration(BaseModel):
    user: UserCreate
    vendor: VendorCreate
