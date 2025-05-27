import jwt
from datetime import timedelta, timezone, datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "GriUtYd3xpyV22L5tkSV3SGk5ZnzBwczNX7Hwxe9b4A"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_pwd_hash(password : str):
    return pwd_context.hash(password)

def verify_pwd (enterd_pwd, hashed_pwd):
    return pwd_context.verify(enterd_pwd, hashed_pwd)