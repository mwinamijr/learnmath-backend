from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from uuid import UUID

from app.models.lesson import Subject
from app.schemas.lesson_schemas import SubjectCreate, SubjectUpdate


def create_subject(db: Session, subject: SubjectCreate):

    new_subject = Subject(
        name=subject.name,
        grade_level=subject.grade_level,
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


def get_all_subjects(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(Subject)
    return query.offset(skip).limit(limit).all()


def get_subject_by_id(db: Session, subject_id: UUID):
    return db.query(Subject).filter(Subject.id == subject_id).first()


def update_subject(db: Session, subject_id: UUID, subject_update: SubjectUpdate):

    subject = get_subject_by_id(db, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    for field, value in subject_update.dict(exclude_unset=True).items():
        setattr(subject, field, value)

    db.commit()
    db.refresh(subject)

    return subject


def delete_subject(db: Session, subject_id: UUID):

    subject = get_subject_by_id(db, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    db.delete(subject)
    db.commit()

    return {"detail": "Subject deleted successfully"}
