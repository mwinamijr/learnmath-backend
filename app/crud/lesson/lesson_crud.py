from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from typing import Union
from uuid import UUID

from app.models.lesson import Lesson, LessonContent, InteractiveLessonVisual
from app.schemas.lesson_schemas import (
    LessonCreate,
    LessonUpdate,
    LessonContentCreate,
    LessonContentUpdate,
    InteractiveLessonCreate,
    InteractiveLessonUpdate,
)


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


def create_lesson_content(db: Session, content: LessonContentCreate):
    new_content = LessonContent(
        lesson_id=content.lesson_id,
        content_type=content.content_type,
        content_data=content.content_data,
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return new_content


def create_interactive_lesson_visual(db: Session, visual: InteractiveLessonCreate):
    new_visual = InteractiveLessonVisual(
        lesson_id=visual.lesson_id,
        content_type=visual.content_type,
        content_data=visual.content_data,
    )

    db.add(new_visual)
    db.commit()
    db.refresh(new_visual)

    return new_visual


def get_all_lessons(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(Lesson)
    return query.offset(skip).limit(limit).all()


def get_all_lesson_contents(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(LessonContent)
    return query.offset(skip).limit(limit).all()


def get_all_visual_lessons(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(InteractiveLessonVisual)
    return query.offset(skip).limit(limit).all()


def get_lesson_by_id(db: Session, lesson_id: UUID):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def get_lesson_content_by_id(db: Session, content_id: UUID):
    return db.query(LessonContent).filter(LessonContent.id == content_id).first()


def get_visual_lesson_by_id(db: Session, visual_id: UUID):
    return (
        db.query(InteractiveLessonVisual)
        .filter(InteractiveLessonVisual.id == visual_id)
        .first()
    )


def update_lesson(db: Session, lesson_id: UUID, lesson_update: LessonUpdate):

    lesson = get_lesson_by_id(db, lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    for field, value in lesson_update.dict(exclude_unset=True).items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)

    return lesson


def update_lesson_content(
    db: Session, content_id: UUID, content_update: LessonContentUpdate
):

    content = db.query(LessonContent).filter(LessonContent.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Lesson content not found")

    for field, value in content_update.dict(exclude_unset=True).items():
        setattr(content, field, value)

    db.commit()
    db.refresh(content)

    return content


def update_visual_lesson(
    db: Session, visual_id: UUID, visual_update: InteractiveLessonUpdate
):

    visual = (
        db.query(InteractiveLessonVisual)
        .filter(InteractiveLessonVisual.id == visual_id)
        .first()
    )

    if not visual:
        raise HTTPException(status_code=404, detail="Visual lesson not found")

    for field, value in visual_update.dict(exclude_unset=True).items():
        setattr(visual, field, value)

    db.commit()
    db.refresh(visual)

    return visual


def delete_lesson(db: Session, lesson_id: UUID):

    lesson = get_lesson_by_id(db, lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()

    return {"detail": "Lesson deleted successfully"}


def delete_lesson_content(db: Session, content_id: UUID):

    content = db.query(LessonContent).filter(LessonContent.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Lesson content not found")

    db.delete(content)
    db.commit()

    return {"detail": "Lesson content deleted successfully"}


def delete_visual_lesson(db: Session, visual_id: UUID):

    visual = (
        db.query(InteractiveLessonVisual)
        .filter(InteractiveLessonVisual.id == visual_id)
        .first()
    )

    if not visual:
        raise HTTPException(status_code=404, detail="Visual lesson not found")

    db.delete(visual)
    db.commit()

    return {"detail": "Visual lesson deleted successfully"}
