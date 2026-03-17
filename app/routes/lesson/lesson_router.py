from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.lesson_schemas import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonContentResponse,
    LessonContentCreate,
    LessonContentUpdate,
    InteractiveLessonResponse,
    InteractiveLessonCreate,
    InteractiveLessonUpdate,
)
from app.crud.lesson.lesson_crud import (
    create_lesson,
    create_lesson_content,
    create_interactive_lesson_visual,
    get_all_lessons,
    get_all_lesson_contents,
    get_all_visual_lessons,
    get_lesson_by_id,
    get_lesson_content_by_id,
    get_visual_lesson_by_id,
    update_lesson,
    update_lesson_content,
    update_visual_lesson,
    delete_lesson,
    delete_lesson_content,
    delete_visual_lesson,
)


router = APIRouter(prefix="/api/lessons", tags=["Lessons"])


@router.get("/", response_model=list[LessonResponse])
def get_all_lessons(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return get_all_lessons(db, skip, limit)


@router.get("/{lesson_id}/contents", response_model=list[LessonContentResponse])
def get_lesson_contents(lesson_id: str, db: Session = Depends(get_db)):
    return get_all_lesson_contents(db, lesson_id)


@router.get("/{lesson_id}/visuals", response_model=list[InteractiveLessonResponse])
def get_visual_lessons(lesson_id: str, db: Session = Depends(get_db)):
    return get_all_visual_lessons(db, lesson_id)


@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_new_lesson(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
):
    return create_lesson(db, lesson_data)


@router.post(
    "/contents",
    response_model=LessonContentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_lesson_content(
    content_data: LessonContentCreate,
    db: Session = Depends(get_db),
):
    return create_lesson_content(db, content_data)


@router.post(
    "/visuals",
    response_model=InteractiveLessonResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_interactive_lesson_visual(
    visual_data: InteractiveLessonCreate,
    db: Session = Depends(get_db),
):
    return create_interactive_lesson_visual(db, visual_data)


@router.get("/{lesson_id}", response_model=LessonResponse)
def read_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/contents/{content_id}", response_model=LessonContentResponse)
def read_lesson_content(content_id: str, db: Session = Depends(get_db)):
    content = get_lesson_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Lesson content not found")
    return content


@router.get("/visuals/{visual_id}", response_model=InteractiveLessonResponse)
def read_interactive_lesson_visual(visual_id: str, db: Session = Depends(get_db)):
    visual = get_visual_lesson_by_id(db, visual_id)
    if not visual:
        raise HTTPException(status_code=404, detail="Visual lesson not found")
    return visual


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


@router.put("/contents/{content_id}", response_model=LessonContentResponse)
def update_existing_lesson_content(
    content_id: str,
    content_data: LessonContentUpdate,
    db: Session = Depends(get_db),
):
    content = get_lesson_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Lesson content not found")
    return update_lesson_content(db, content, content_data)


@router.put("/visuals/{visual_id}", response_model=InteractiveLessonResponse)
def update_existing_interactive_lesson_visual(
    visual_id: str,
    visual_data: InteractiveLessonUpdate,
    db: Session = Depends(get_db),
):
    visual = get_visual_lesson_by_id(db, visual_id)
    if not visual:
        raise HTTPException(status_code=404, detail="Visual lesson not found")
    return update_visual_lesson(db, visual, visual_data)


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    delete_lesson(db, lesson)
    return None


@router.delete("/contents/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_lesson_content(content_id: str, db: Session = Depends(get_db)):
    content = get_lesson_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Lesson content not found")
    delete_lesson_content(db, content)
    return None


@router.delete("/visuals/{visual_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_interactive_lesson_visual(
    visual_id: str, db: Session = Depends(get_db)
):
    visual = get_visual_lesson_by_id(db, visual_id)
    if not visual:
        raise HTTPException(status_code=404, detail="Visual lesson not found")
    delete_visual_lesson(db, visual)
    return None
