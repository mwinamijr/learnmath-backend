import uuid
import enum
from sqlalchemy import Column, Enum, String, Integer, ForeignKey, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class GradeLevel(enum.Enum):
    primary = "primary"
    o_level = "o-level"
    a_level = "a-level"


class LessonType(enum.Enum):
    video = "video"
    interactive = "interactive"
    game = "game"
    read = "read"


class DifficultyLevel(enum.Enum):
    easy = "easy"
    intermediate = "intermediate"
    hard = "hard"


# subject
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    grade_level = Column(Enum(GradeLevel))


# topic
class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject = Column(ForeignKey("subjects.id"), nullable=False)
    class_level = Column(Integer)
    name = Column(String(255), nullable=False)
    order_index = Column(Integer)
    description = Column(Text, nullable=True)


class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(ForeignKey("topics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    order_index = Column(Integer)


# lesson
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sub_topic = Column(ForeignKey("subtopics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer)
    lesson_type = Column(Enum(LessonType), default=LessonType.read)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.easy)
    estimated_minutes = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
