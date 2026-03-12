from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from typing import Union
from uuid import UUID

from app.models.user import User
from app.schemas.user_schemas import AdminUserCreate, RegisterUser, UserUpdate
from app.utils.password import hash_password


def create_user(db: Session, user: Union[AdminUserCreate, RegisterUser]):

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken.")

    if user.email:
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered.")

    if db.query(User).filter(User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already exists.")

    new_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        first_name=getattr(user, "first_name", None),
        last_name=getattr(user, "last_name", None),
        hashed_password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(User)
    return query.offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: UUID, user_update: UserUpdate):

    user = get_user_by_id(db, user_id)

    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    # hash password if it exists
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: UUID):

    user = get_user_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
