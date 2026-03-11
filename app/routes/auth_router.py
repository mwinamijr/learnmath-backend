from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models.user import UserRole
from app.dependancies.auth_dependancies import is_system_not_initialized
from app.schemas.user_schemas import UserCreate, UserLogin, Token, UserResponse
from app.crud.user_crud import create_user
from app.utils.jwt_handler import create_access_token
from app.utils.auth import authenticate_user


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    return create_user(db, user)


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):

    user = authenticate_user(
        user_login.phone_number,
        user_login.password,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/initialize",
    response_model=UserResponse,
    tags=["Initialization"],
)
def initialize_system(
    admin_data: UserCreate,
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
