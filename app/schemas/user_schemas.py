import re
from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime

from app.models.user import TeacherCategory, UserRole


class UserBase(BaseModel):
    username: constr(min_length=4, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: str
    first_name: Optional[constr(max_length=50)] = None
    last_name: Optional[constr(max_length=50)] = None
    role: UserRole

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v):
        if v == "":
            return None
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):

        pattern = r"^\+255\d{9}$"

        if not re.match(pattern, v):
            raise ValueError(
                "Phone number must be in international format like +255XXXXXXXXX"
            )

        return v


class AdminUserCreate(UserBase):
    password: str
    role: UserRole


class RegisterUser(UserBase):
    password: str
    role: Literal["student", "teacher"]


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
    teacher_category: Optional[TeacherCategory] = None
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
