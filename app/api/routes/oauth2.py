import jwt
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError
import datetime
from datetime import timedelta

SECRET_KEY = "GriUtYd3xpyV22L5tkSV3SGk5ZnzBwczNX7Hwxe9b4A"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt