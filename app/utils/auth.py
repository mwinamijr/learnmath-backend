from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.password import verify_password


def authenticate_user(phone_number: str, password: str, db: Session):
    """
    Authenticate a user by verifying their phone number and password.

    Args:
        phone number (str): The phone number provided by the user.
        password (str): The plain-text password provided by the user.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The authenticated user object if successful, None otherwise.
    """
    user = db.query(User).filter(User.phone_number == phone_number).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
