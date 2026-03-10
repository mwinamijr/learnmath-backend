from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.password import hash_password


def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400, detail="User with this email already registerd."
        )
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(
            status_code=400, detail="User with this phone number already exist."
        )

    new_user = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hash_password(user.password),
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query: Query = db.query(User)
    return query.offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: str, user: UserUpdate):
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    for field, value in user.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()

    return {"message": "User deleted successfully"}
