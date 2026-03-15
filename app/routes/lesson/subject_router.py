from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lesson_schemas import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
)
from app.crud.lesson.subject_crud import (
    create_subject,
    get_subject_by_id,
    update_subject,
    delete_subject,
)

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_new_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
):
    return create_subject(db, subject_data)


@router.get("/{subject_id}", response_model=SubjectResponse)
def read_subject(subject_id: str, db: Session = Depends(get_db)):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_existing_subject(
    subject_id: str,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return update_subject(db, subject, subject_data)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_subject(subject_id: str, db: Session = Depends(get_db)):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    delete_subject(db, subject)
    return None
