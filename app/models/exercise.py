import uuid
import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    Text,
    text,
)

from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base
from app.models.lesson import DifficultyLevel


class QuestionType(enum.Enum):
    """
    Defines the different formats an exercise question can take.

    mcq:
        Multiple choice question with predefined options.

    drag_drop:
        Students drag objects (apples, blocks, shapes) to solve the problem.

    interactive:
        Fully interactive visual problem solved using animations or manipulable objects.
    """

    mcq = "multiple choice question"
    drag_drop = "drag and drop"
    interactive = "interactive"


class Exercise(Base):
    """
    Represents a single exercise belonging to a lesson.

    Each exercise contains:
    - The question text
    - The type of interaction required
    - The correct answer stored as JSON
    - Visual configuration for rendering the exercise
    - Difficulty level inherited from the lesson system

    The `correct_answer` field is stored as JSONB so that it can support
    multiple answer structures such as:
        - simple numeric answers
        - multiple choice options
        - drag-and-drop configurations
    """

    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_text = Column(Text, nullable=False)

    question_type = Column(
        Enum(QuestionType),
        nullable=False,
    )

    correct_answer = Column(
        JSONB,
        nullable=False,
    )

    visual_type = Column(
        String(255),
        nullable=True,
    )

    difficulty = Column(
        Enum(DifficultyLevel),
        nullable=False,
    )


class ExerciseAttempt(Base):
    """
    Tracks a student's attempt at solving a specific exercise.

    This table stores:
    - The answer submitted by the student
    - Whether the answer was correct
    - Score awarded
    - Time taken to answer

    This enables analytics such as:
    - accuracy rates
    - average solving time
    - difficulty tuning
    """

    __tablename__ = "exercise_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    exercise_id = Column(
        UUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
    )

    answer = Column(
        JSONB,
        nullable=False,
    )

    is_correct = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    score = Column(
        Integer,
        default=0,
        nullable=False,
    )

    time_taken = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
