from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from typing import Union
from uuid import UUID

from app.models.lesson import Lesson
from app.schemas.lesson_schemas import LessonCreate, LessonUpdate


def create_lesson(db: Session, lesson: LessonCreate):
    new_lesson = Lesson(
        name=lesson.name,
        description=lesson.description,
        order_index=lesson.order_index,
        sub_topic=lesson.sub_topic,
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


def get_all_lessons(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(Lesson)
    return query.offset(skip).limit(limit).all()


def get_lesson_by_id(db: Session, lesson_id: UUID):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def update_lesson(db: Session, lesson_id: UUID, lesson_update: LessonUpdate):

    lesson = get_lesson_by_id(db, lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    for field, value in lesson_update.dict(exclude_unset=True).items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)

    return lesson


def delete_lesson(db: Session, lesson_id: UUID):

    lesson = get_lesson_by_id(db, lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()

    return {"detail": "Lesson deleted successfully"}
