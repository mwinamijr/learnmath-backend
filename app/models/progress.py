import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Integer,
    Float,
    ForeignKey,
    TIMESTAMP,
    text,
)

from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class LessonProgress(Base):
    """
    Tracks a student's progress within a specific lesson.

    This table records:
    - Whether the lesson has been completed
    - The score achieved in the lesson
    - The timestamp of completion

    This allows the platform to:
    - Track learning progress
    - Resume unfinished lessons
    - Compute topic and course progress
    """

    __tablename__ = "lesson_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    completed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    score = Column(
        Integer,
        default=0,
        nullable=False,
    )

    completed_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )


class TopicProgress(Base):
    """
    Tracks overall progress of a student within a topic/module.

    A topic typically contains multiple lessons. This table stores:
    - Percentage completion of the topic
    - The last lesson the student accessed

    Used to quickly resume learning and display progress bars.
    """

    __tablename__ = "topic_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )

    progress_percent = Column(
        Float,
        default=0.0,
        nullable=False,
    )

    last_lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id"),
        nullable=True,
    )


class Streak(Base):
    """
    Tracks a user's learning streak.

    Streaks encourage daily learning by tracking:
    - Current consecutive learning days
    - Longest streak achieved
    - Last day the student was active

    Used for gamification and rewards.
    """

    __tablename__ = "streaks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    current_streak = Column(
        Integer,
        default=0,
        nullable=False,
    )

    longest_streak = Column(
        Integer,
        default=0,
        nullable=False,
    )

    last_activity_date = Column(
        Date,
        nullable=True,
    )


class Leaderboard(Base):
    """
    Stores leaderboard rankings for users.

    Leaderboards rank students based on accumulated points
    earned from exercises, lessons, and achievements.

    This enables:
    - Friendly competition
    - Motivation through ranking
    - Weekly or global rankings
    """

    __tablename__ = "leaderboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    points = Column(
        Integer,
        default=0,
        nullable=False,
    )

    rank = Column(
        Integer,
        default=0,
        nullable=False,
    )
