from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_LENGTH = 72  # bcrypt limit


def hash_password(password: str) -> str:
    # truncate automatically
    truncated_password = password[:MAX_BCRYPT_LENGTH]
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated_password = plain_password[:MAX_BCRYPT_LENGTH]
    return pwd_context.verify(truncated_password, hashed_password)
