import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import datetime
from datetime import timedelta
from app.models import TokenPayload
from fastapi import Depends, status, HTTPException  

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = "GriUtYd3xpyV22L5tkSV3SGk5ZnzBwczNX7Hwxe9b4A"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenPayload()
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token : str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})
    return verify_access_token(token, credentials_exception)
