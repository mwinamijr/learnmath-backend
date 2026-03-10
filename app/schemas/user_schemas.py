from enum import Enum
from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class UserBase(BaseModel):
    username: constr(min_length=5, max_length=50)
    email: EmailStr
    phone: constr(min_length=10, max_length=13)
    first_name: constr(max_length=50) = None
    last_name: constr(max_length=50) = None
    role: UserRole


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: constr(max_length=50) = None
    last_name: constr(max_length=50) = None
    password: constr(min_length=8, max_length=128) = None
    phone: constr(min_length=10, max_length=13) = None
    email: EmailStr = None
    role: UserRole = None


class UserResponse(UserBase):
    id: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone: constr(min_length=10, max_length=13)
    password: constr(min_length=8, max_length=128)


class Token(BaseModel):
    access: str
    refresh: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
