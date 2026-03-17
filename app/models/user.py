import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from app.db.database import Base
from app.db.enums import UserRole, TeacherCategory


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(13), unique=True, index=True)
    hashed_password = Column(String(128))
    role = Column(String(50), nullable=False)
    teacher_category = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    @validates("role")
    def validate_role(self, key, value):
        if value not in UserRole.__members__:
            raise ValueError(f"Invalid role: {value}")
        return value

    @validates("teacher_category")
    def validate_teacher_category(self, key, value):
        if value is not None and value not in TeacherCategory.__members__:
            raise ValueError(f"Invalid teacher category: {value}")
        return value


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    bio = Column(String(500), nullable=True)
    age = Column(Integer, nullable=True)
    grade = Column(String(10), nullable=True)
    avatar = Column(String(255), nullable=True)
