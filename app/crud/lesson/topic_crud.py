from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from typing import Union
from uuid import UUID

from app.models.lesson import Topic
from app.schemas.lesson_schemas import TopicCreate, TopicUpdate


def create_topic(db: Session, topic: TopicCreate):

    new_topic = Topic(
        name=topic.name,
        grade_level=topic.grade_level,
        subject=topic.subject,
    )

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic


def get_all_topics(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(Topic)
    return query.offset(skip).limit(limit).all()


def get_topic_by_id(db: Session, topic_id: UUID):
    return db.query(Topic).filter(Topic.id == topic_id).first()


def update_topic(db: Session, topic_id: UUID, topic_update: TopicUpdate):

    topic = get_topic_by_id(db, topic_id)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    for field, value in topic_update.dict(exclude_unset=True).items():
        setattr(topic, field, value)

    db.commit()
    db.refresh(topic)

    return topic


def delete_topic(db: Session, topic_id: UUID):

    topic = get_topic_by_id(db, topic_id)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.delete(topic)
    db.commit()

    return {"detail": "Topic deleted successfully"}
