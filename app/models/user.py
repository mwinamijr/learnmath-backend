import uuid
import enum
from sqlalchemy import Column, String, Boolean, Enum, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class UserRole(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class TeacherCategory(enum.Enum):
    pending = "pending"  # joined, not yet approved
    approved = "approved"  # verified teacher
    starter = "starter"  # teacher with some courses, but not yet popular
    paid_courses = "paid_courses"  # teacher has paid courses but not yet popular
    popular = "popular"  # high-reputation teacher
    vip = "vip"  # optional, high-reputation


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(13), unique=True, index=True)
    hashed_password = Column(String(128))
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
