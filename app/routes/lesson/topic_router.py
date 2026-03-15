from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lesson_schemas import (
    TopicCreate,
    TopicUpdate,
    TopicResponse,
)
from app.crud.lesson.topic_crud import (
    create_topic,
    get_topic_by_id,
    update_topic,
    delete_topic,
)

router = APIRouter(prefix="/api/topics", tags=["Topics"])


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_new_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
):
    return create_topic(db, topic_data)


@router.get("/{topic_id}", response_model=TopicResponse)
def read_topic(topic_id: str, db: Session = Depends(get_db)):
    topic = get_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/{topic_id}", response_model=TopicResponse)
def update_existing_topic(
    topic_id: str,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
):
    topic = get_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return update_topic(db, topic, topic_data)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_topic(topic_id: str, db: Session = Depends(get_db)):
    topic = get_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    delete_topic(db, topic)
    return None
