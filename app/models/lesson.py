import uuid
import enum

from sqlalchemy import Column, Enum, String, Integer, ForeignKey, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base


class GradeLevel(enum.Enum):
    """
    Represents the education level the subject belongs to.

    primary:
        Primary school level mathematics.

    o_level:
        Secondary school (Ordinary level).

    a_level:
        Advanced secondary school mathematics.
    """

    primary = "primary"
    o_level = "o-level"
    a_level = "a-level"


class LessonType(enum.Enum):
    """
    Defines the format used to deliver a lesson.

    video:
        Lesson is presented through video explanation.

    interactive:
        Lesson uses visual objects and interaction.

    game:
        Lesson is delivered as a math mini-game.

    read:
        Lesson is text-based explanation with diagrams.
    """

    video = "video"
    interactive = "interactive"
    game = "game"
    read = "read"


class DifficultyLevel(enum.Enum):
    """
    Represents the difficulty level of a lesson or exercise.

    easy:
        Beginner-level problems.

    intermediate:
        Medium difficulty problems.

    hard:
        Advanced or challenging problems.
    """

    easy = "easy"
    intermediate = "intermediate"
    hard = "hard"


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

    name = Column(
        String(255),
        nullable=False,
    )

    grade_level = Column(
        Enum(GradeLevel),
        nullable=False,
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

    class_level = Column(
        Integer,
        nullable=False,
    )

    name = Column(
        String(255),
        nullable=False,
    )

    order_index = Column(
        Integer,
        default=0,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
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

    name = Column(
        String(255),
        nullable=False,
    )

    order_index = Column(
        Integer,
        default=0,
        nullable=False,
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

    name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    order_index = Column(
        Integer,
        default=0,
        nullable=False,
    )

    lesson_type = Column(
        Enum(LessonType),
        default=LessonType.read,
        nullable=False,
    )

    difficulty = Column(
        Enum(DifficultyLevel),
        default=DifficultyLevel.easy,
        nullable=False,
    )

    estimated_minutes = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
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

    object_type = Column(
        String(255),
        nullable=False,
    )

    object_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    interaction_type = Column(
        String(255),
        nullable=True,
    )


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

    content_type = Column(
        Enum(LessonType),
        nullable=False,
    )

    content_data = Column(
        JSONB,
        nullable=False,
    )

    order_index = Column(
        Integer,
        default=0,
        nullable=False,
    )
