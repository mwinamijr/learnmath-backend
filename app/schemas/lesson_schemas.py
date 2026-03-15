from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID

from app.models.lesson import GradeLevel, LessonType, DifficultyLevel


class SubjectBase(BaseModel):
    name: constr(max_length=255)
    grade_level: GradeLevel


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    name: Optional[constr(max_length=255)] = None
    grade_level: Optional[GradeLevel] = None


class SubjectResponse(SubjectBase):
    id: UUID

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    subject_id: UUID
    name: constr(max_length=255)
    class_level: int
    description: Optional[str] = None


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    name: Optional[constr(max_length=255)] = None
    class_level: Optional[int] = None
    description: Optional[str] = None


class TopicResponse(TopicBase):
    id: UUID

    class Config:
        from_attributes = True


class SubtopicBase(BaseModel):
    topic_id: UUID
    name: constr(max_length=255)
    order_index: int


class SubtopicCreate(SubtopicBase):
    pass


class SubtopicUpdate(SubtopicBase):
    name: Optional[constr(max_length=255)] = None
    order_index: Optional[int] = None


class SubtopicResponse(SubtopicBase):
    id: UUID

    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    sub_topic_id: UUID
    name: constr(max_length=255)
    description: Optional[str] = None
    order_index: int
    lesson_type: LessonType
    difficulty_level: DifficultyLevel


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    lesson_type: Optional[LessonType] = None
    difficulty_level: Optional[DifficultyLevel] = None


class LessonResponse(LessonBase):
    id: UUID

    class Config:
        from_attributes = True
