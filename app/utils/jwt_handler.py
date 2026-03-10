import enum
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.models.user import User, UserRole
from app.config import settings


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    to_encode = {
        key: (value.value if isinstance(value, enum.Enum) else value)
        for key, value in to_encode.items()
    }

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username = payload.get("sub")
    role = UserRole(payload.get(role))
    return {"username": username, "role": role}
