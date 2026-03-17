from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.db.database import Base
from app.db.enums import (
    lesson_type_enum,
    difficulty_level_enum,
    grade_level_enum,
    user_role_enum,
    teacher_category_enum,
)
from app.config import settings
from app.models.user import User, Profile
from app.models.lesson import (
    Subject,
    Topic,
    Subtopic,
    Lesson,
    LessonContent,
    InteractiveLessonVisual,
)

# from app.models.exercise import Exercise, ExerciseAttempt
# from app.models.progress import LessonProgress, TopicProgress, Streak, Leaderboard
# from app.models.reward import Reward, Badge, UserBadge

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

from alembic.autogenerate import renderers


@renderers.dispatch_for("type")
def render_type(autogen_type, autogen_context):
    """
    This prevents Alembic from generating inline ENUMs
    and instead references our pre-defined ENUMs.
    """
    enum_name = str(autogen_type)
    if enum_name in (
        "lessontype",
        "difficultylevel",
        "gradelevel",
        "userrole",
        "teachercategory",
    ):
        # just render the ENUM type name in SQL
        return enum_name
    return None  # fallback to default rendering


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Make sure enums exist BEFORE using them in tables
        for enum_type in (
            lesson_type_enum,
            difficulty_level_enum,
            grade_level_enum,
            user_role_enum,
            teacher_category_enum,
        ):
            enum_type.create(connection, checkfirst=True)

        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
