import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    Text,
    text,
    Index,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.enums import lesson_type_enum, difficulty_level_enum, grade_level_enum


class Subject(Base):
    """
    Represents a high-level academic subject.

    Example subjects:
        - Mathematics
        - Physics
        - Chemistry

    Each subject belongs to a specific grade level
    (primary, O-level, or A-level).
    """

    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    grade_level = Column(grade_level_enum, nullable=False)

    # RELATIONSHIPS
    topics = relationship(
        "Topic",
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    # CONSTRAINTS + INDEXES
    __table_args__ = (
        UniqueConstraint("name", "grade_level", name="uq_subject_name_grade"),
        Index("idx_subject_grade", "grade_level"),
    )


class Topic(Base):
    """
    Represents a major topic within a subject.

    Example:
        Subject: Mathematics
        Topic: Algebra

    Topics are organized by class level and ordered
    within the subject.
    """

    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )

    class_level = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    description = Column(Text)

    # RELATIONSHIPS
    subject = relationship("Subject", back_populates="topics")

    subtopics = relationship(
        "Subtopic",
        back_populates="topic",
        cascade="all, delete-orphan",
    )

    # CONSTRAINTS + INDEXES
    __table_args__ = (
        UniqueConstraint(
            "subject_id", "class_level", "name", name="uq_topic_per_class"
        ),
        Index("idx_topic_subject", "subject_id"),
        Index("idx_topic_class_level", "class_level"),
    )


class Subtopic(Base):
    """
    Represents a smaller subdivision of a topic.

    Example:
        Topic: Algebra
        Subtopic: Linear Equations

    Subtopics help organize lessons into manageable
    learning units.
    """

    __tablename__ = "subtopics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # RELATIONSHIPS
    topic = relationship("Topic", back_populates="subtopics")

    lessons = relationship(
        "Lesson",
        back_populates="subtopic",
        cascade="all, delete-orphan",
    )

    # CONSTRAINTS + INDEXES
    __table_args__ = (
        UniqueConstraint("topic_id", "name", name="uq_subtopic_name"),
        Index("idx_subtopic_topic", "topic_id"),
    )


class Lesson(Base):
    """
    Represents an individual lesson within a subtopic.

    Lessons contain:
        - Explanation content
        - Interactive visuals
        - Exercises
        - Games or videos

    Lessons are ordered sequentially within a subtopic
    to create a structured learning path.
    """

    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    subtopic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)
    description = Column(Text)

    order_index = Column(Integer, default=0, nullable=False)

    lesson_type = Column(lesson_type_enum, nullable=False)
    difficulty = Column(difficulty_level_enum, nullable=False)

    estimated_minutes = Column(Integer)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )

    # RELATIONSHIPS
    subtopic = relationship("Subtopic", back_populates="lessons")

    contents = relationship(
        "LessonContent",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    visuals = relationship(
        "InteractiveLessonVisual",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    # CONSTRAINTS + INDEXES
    __table_args__ = (
        UniqueConstraint("subtopic_id", "order_index", name="uq_lesson_order"),
        Index("idx_lesson_subtopic", "subtopic_id"),
        Index("idx_lesson_type", "lesson_type"),
        Index("idx_lesson_difficulty", "difficulty"),
    )


class InteractiveLessonVisual(Base):
    """
    Stores configuration for interactive objects used in a lesson.

    These visuals are used by the frontend animation engine (PixiJS)
    to render manipulable objects such as:

        - apples for counting
        - blocks for addition
        - groups for multiplication

    Example configuration:
        object_type = "apple"
        object_count = 3
        interaction_type = "addition"
    """

    __tablename__ = "lesson_visuals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    object_type = Column(String(255), nullable=False)
    object_count = Column(Integer, default=0, nullable=False)
    interaction_type = Column(String(255))

    # RELATIONSHIPS
    lesson = relationship("Lesson", back_populates="visuals")

    # INDEXES
    __table_args__ = (Index("idx_visual_lesson", "lesson_id"),)


class LessonContent(Base):
    """
    Stores the ordered content blocks that make up a lesson.

    A lesson can contain multiple pieces of content such as:

        - text explanation
        - animations
        - videos
        - interactive demonstrations

    The `content_data` column uses JSONB so the frontend
    can dynamically render different content types.

    Example JSON:

    {
        "text": "Adding 2 apples and 3 apples gives 5 apples",
        "objects": ["apple", "apple", "apple"]
    }

    The `order_index` controls the sequence in which the
    content blocks appear inside the lesson.
    """

    __tablename__ = "lesson_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    content_type = Column(lesson_type_enum, nullable=False)

    content_data = Column(JSONB, nullable=False)

    order_index = Column(Integer, default=0, nullable=False)

    # RELATIONSHIPS
    lesson = relationship("Lesson", back_populates="contents")

    # CONSTRAINTS + INDEXES
    __table_args__ = (
        UniqueConstraint("lesson_id", "order_index", name="uq_lesson_content_order"),
        Index("idx_content_lesson", "lesson_id"),
    )
