from fastapi import Depends, HTTPException, status

from app.models.user import User, UserRole
from app.dependancies.auth_dependancies import get_current_user


def admin_only(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user


def teacher_only(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher privileges required",
        )

    return current_user


def student_only(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student privileges required",
        )

    return current_user


def admin_or_teacher(current_user: User = Depends(get_current_user)):

    if current_user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Teacher privileges required",
        )

    return current_user


def admin_or_self(
    user_id: str,
    current_user: User = Depends(get_current_user),
):

    if current_user.role == UserRole.admin:
        return current_user

    if str(current_user.id) == str(user_id):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only admin or the account owner can perform this action",
    )
