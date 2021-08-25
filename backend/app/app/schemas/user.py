import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    full_name: str
    password: str
    company: Optional[str] = "Private individual"
    country: str
    is_superuser: bool = False


# Properties to receive via API on update
class UserUpdate(UserBase):
    hashed_password: Optional[str] = None
    company: Optional[str]
    country: Optional[str]


class UserInDBBase(UserBase):
    id: Optional[int] = None


    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    company: Optional[str] = "Private individual"
    country: str
    last_updated: datetime.datetime
    created: datetime.datetime


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    last_updated: datetime.datetime
    created: datetime.datetime
