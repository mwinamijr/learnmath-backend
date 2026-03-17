import uuid
import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    String,
    Integer,
    ForeignKey,
    Text,
    Index,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.database import Base
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


class Question(Base):
    """
    Central reusable question bank.

    A single question can be used in:
    - exercises
    - quizzes
    - exams

    Supports all formats via JSONB.
    """

    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )

    question_text = Column(Text, nullable=False)

    question_type = Column(
        Enum(QuestionType),
        nullable=False,
    )

    data = Column(JSONB, nullable=False)
    # contains options, drag config, pixi JSON etc

    correct_answer = Column(JSONB, nullable=False)

    difficulty = Column(
        Enum(DifficultyLevel),
        nullable=False,
    )

    points = Column(Integer, default=1, nullable=False)

    # INDEXES
    __table_args__ = (
        Index("idx_question_lesson", "lesson_id"),
        Index("idx_question_difficulty", "difficulty"),
    )


class Exercise(Base):
    """
    Practice set inside a lesson.

    Contains multiple questions.
    Not timed.
    """

    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(255), nullable=False)

    difficulty = Column(Enum(DifficultyLevel), nullable=False)

    # RELATION
    questions = relationship("ExerciseQuestion", back_populates="exercise")

    __table_args__ = (Index("idx_exercise_lesson", "lesson_id"),)


class Exercise(Base):
    """
    Practice set inside a lesson.

    Contains multiple questions.
    Not timed.
    """

    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(255), nullable=False)

    difficulty = Column(Enum(DifficultyLevel), nullable=False)

    # RELATION
    questions = relationship("ExerciseQuestion", back_populates="exercise")

    __table_args__ = (Index("idx_exercise_lesson", "lesson_id"),)


class ExerciseQuestion(Base):
    """
    Links questions to an exercise.
    Allows ordering.
    """

    __tablename__ = "exercise_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    exercise_id = Column(
        UUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    order_index = Column(Integer, default=0)

    # RELATIONSHIPS
    exercise = relationship("Exercise", back_populates="questions")
    question = relationship("Question")

    __table_args__ = (UniqueConstraint("exercise_id", "question_id"),)


class Quiz(Base):
    """
    Short assessment (not strictly timed).
    """

    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"))

    title = Column(String(255), nullable=False)

    total_marks = Column(Integer, default=0)

    time_limit = Column(Integer)  # optional (seconds)

    __table_args__ = (Index("idx_quiz_lesson", "lesson_id"),)


class Exam(Base):
    """
    Formal timed exam.

    Example:
    - Midterm
    - Final exam
    """

    __tablename__ = "exams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(255), nullable=False)

    total_marks = Column(Integer, nullable=False)

    duration_minutes = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)

    __table_args__ = (Index("idx_exam_active", "is_active"),)


class Exam(Base):
    """
    Formal timed exam.

    Example:
    - Midterm
    - Final exam
    """

    __tablename__ = "exams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(255), nullable=False)

    total_marks = Column(Integer, nullable=False)

    duration_minutes = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)

    __table_args__ = (Index("idx_exam_active", "is_active"),)
