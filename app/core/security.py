import bcrypt
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

_BCRYPT_MAX_PASSWORD_BYTES = 72


def verify_password(plain_password: str, hash_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hash_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def get_hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > _BCRYPT_MAX_PASSWORD_BYTES:
        raise ValueError("Password cannot be longer than 72 bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def create_access_token(subject: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": subject, "exp": exp}
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return payload.get("sub")
    except JWTError:
        return None
