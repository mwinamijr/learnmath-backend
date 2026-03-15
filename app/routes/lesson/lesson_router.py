from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lesson_schemas import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
)
from app.crud.lesson.lesson_crud import (
    create_lesson,
    get_lesson_by_id,
    update_lesson,
    delete_lesson,
)


router = APIRouter(prefix="/api/lessons", tags=["Lessons"])


@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_new_lesson(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
):
    return create_lesson(db, lesson_data)


@router.get("/{lesson_id}", response_model=LessonResponse)
def read_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.put("/{lesson_id}", response_model=LessonResponse)
def update_existing_lesson(
    lesson_id: str,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
):
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return update_lesson(db, lesson, lesson_data)


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    delete_lesson(db, lesson)
    return None
