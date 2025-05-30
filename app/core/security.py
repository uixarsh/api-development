import jwt
from datetime import timedelta, timezone, datetime
from passlib.context import CryptContext
from typing import Any
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM = "HS256"

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_pwd_hash(password : str):
    return pwd_context.hash(password)

def verify_pwd (enterd_pwd, hashed_pwd):
    return pwd_context.verify(enterd_pwd, hashed_pwd)