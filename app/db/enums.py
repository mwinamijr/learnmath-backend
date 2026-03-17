import enum

from sqlalchemy.dialects.postgresql import ENUM


# User Enums
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


# Lesson enums
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


grade_level_enum = ENUM(GradeLevel, name="gradelevel", create_type=False)
lesson_type_enum = ENUM(LessonType, name="lessontype", create_type=False)
difficulty_level_enum = ENUM(DifficultyLevel, name="difficultylevel", create_type=False)
user_role_enum = ENUM(UserRole, name="userrole", create_type=False)
teacher_category_enum = ENUM(TeacherCategory, name="teachercategory", create_type=False)
