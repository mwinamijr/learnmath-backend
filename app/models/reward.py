import uuid
import enum

from sqlalchemy import (
    Column,
    Enum,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    Text,
    text,
)

from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class RewardType(enum.Enum):
    """
    Defines the types of rewards that can be granted to a user.

    star:
        Basic reward typically given for completing exercises.

    coin:
        Virtual currency that may be used to unlock items or bonuses.

    xp:
        Experience points used to measure overall learning progress.
    """

    star = "star"
    coin = "coin"
    xp = "xp"


class Reward(Base):
    """
    Represents a reward that can be granted to a user.

    Rewards are used in the gamification system to motivate students.
    They may be granted when a student:
        - completes a lesson
        - answers exercises correctly
        - maintains a learning streak
        - earns a badge

    The `value` column determines how much of the reward is granted.
    """

    __tablename__ = "rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    reward_type = Column(
        Enum(RewardType, name="reward_type_enum"),
        nullable=False,
    )

    value = Column(
        Integer,
        default=0,
        nullable=False,
    )


class Badge(Base):
    """
    Represents an achievement badge that users can earn.

    Badges are awarded when a user reaches certain milestones such as:
        - completing a topic
        - achieving high accuracy
        - maintaining streaks
        - solving difficult exercises

    The `icon_url` field stores the badge image used in the UI.
    """

    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    icon_url = Column(
        String(255),
        nullable=True,
    )


class UserBadge(Base):
    """
    Junction table linking users to badges they have earned.

    This table records:
        - which user earned a badge
        - which badge was earned
        - when the badge was awarded

    A user should not earn the same badge more than once,
    so a unique constraint is typically enforced at the database level.
    """

    __tablename__ = "user_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    badge_id = Column(
        UUID(as_uuid=True),
        ForeignKey("badges.id", ondelete="CASCADE"),
        nullable=False,
    )

    earned_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
