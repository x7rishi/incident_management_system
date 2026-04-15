import uuid
from pydantic import BaseModel, EmailStr, ConfigDict,Field
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = Field(None, max_length=100)
    is_active: bool = True 


class UserCreate(UserBase):
    password: str = Field(...,min_length=8)

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True)

