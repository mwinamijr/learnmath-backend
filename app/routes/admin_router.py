from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.dependancies.permissions import admin_only
from app.models.user import User, UserRole
from app.dependancies.auth_dependancies import is_system_not_initialized
from app.schemas.user_schemas import AdminUserCreate, UserResponse
from app.crud.user_crud import create_user


router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post(
    "/initialize",
    response_model=UserResponse,
)
def initialize_system(
    admin_data: AdminUserCreate,
    secret_key: str,
    db: Session = Depends(get_db),
    system_not_initialized: None = Depends(is_system_not_initialized),
):

    if secret_key != settings.INITIALIZE_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    # Force admin role
    admin_data.role = UserRole.admin

    admin_user = create_user(db, admin_data)

    return admin_user


@router.post("/register", response_model=UserResponse)
def create_admin_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only),
):
    user.role = UserRole.admin
    return create_user(db, user)
