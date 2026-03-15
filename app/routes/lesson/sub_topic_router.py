from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lesson_schemas import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    TopicCreate,
    TopicUpdate,
    TopicResponse,
    SubtopicCreate,
    SubtopicUpdate,
    SubtopicResponse,
    LessonCreate,
    LessonUpdate,
    LessonResponse,
)
from app.crud.lesson.sub_topic_crud import (
    create_subtopic,
    get_subtopic_by_id,
    update_subtopic,
    delete_subtopic,
)

router = APIRouter(prefix="/api/subtopics", tags=["Subtopics"])


@router.post("/", response_model=SubtopicResponse, status_code=status.HTTP_201_CREATED)
def create_new_subtopic(
    subtopic_data: SubtopicCreate,
    db: Session = Depends(get_db),
):
    return create_subtopic(db, subtopic_data)


@router.get("/{subtopic_id}", response_model=SubtopicResponse)
def read_subtopic(subtopic_id: str, db: Session = Depends(get_db)):
    subtopic = get_subtopic_by_id(db, subtopic_id)
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


@router.put("/{subtopic_id}", response_model=SubtopicResponse)
def update_existing_subtopic(
    subtopic_id: str,
    subtopic_data: SubtopicUpdate,
    db: Session = Depends(get_db),
):
    subtopic = get_subtopic_by_id(db, subtopic_id)
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return update_subtopic(db, subtopic_id, subtopic_data)


@router.delete("/{subtopic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_subtopic(subtopic_id: str, db: Session = Depends(get_db)):
    subtopic = get_subtopic_by_id(db, subtopic_id)
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    delete_subtopic(db, subtopic)
    return None
