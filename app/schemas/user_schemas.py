from enum import Enum
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserBase(BaseModel):
    username: constr(min_length=5, max_length=50)
    email: EmailStr
    phone_number: constr(min_length=10, max_length=13)
    first_name: Optional[constr(max_length=50)] = None
    last_name: Optional[constr(max_length=50)] = None
    role: UserRole


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: Optional[constr(max_length=50)] = None
    last_name: Optional[constr(max_length=50)] = None
    password: Optional[constr(min_length=8, max_length=128)] = None
    phone_number: Optional[constr(min_length=10, max_length=13)] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone_number: constr(min_length=10, max_length=13)
    password: constr(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
