from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from uuid import UUID

from app.models.lesson import Subtopic
from app.schemas.lesson_schemas import SubtopicCreate, SubtopicUpdate


def create_subtopic(db: Session, subtopic: SubtopicCreate):

    new_subtopic = Subtopic(
        name=subtopic.name,
        topic=subtopic.topic,
    )

    db.add(new_subtopic)
    db.commit()
    db.refresh(new_subtopic)

    return new_subtopic


def get_all_subtopics(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(Subtopic)
    return query.offset(skip).limit(limit).all()


def get_subtopic_by_id(db: Session, subtopic_id: UUID):
    return db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()


def update_subtopic(db: Session, subtopic_id: UUID, subtopic_update: SubtopicUpdate):
    subtopic = get_subtopic_by_id(db, subtopic_id)

    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    for field, value in subtopic_update.dict(exclude_unset=True).items():
        setattr(subtopic, field, value)

    db.commit()
    db.refresh(subtopic)

    return subtopic


def delete_subtopic(db: Session, subtopic_id: UUID):
    subtopic = get_subtopic_by_id(db, subtopic_id)

    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    db.delete(subtopic)
    db.commit()
    return {"detail": "Subtopic deleted successfully"}
