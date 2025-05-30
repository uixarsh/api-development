from fastapi import APIRouter, status, HTTPException, Depends
from app.core.db import SessionDep
from app.models import User, Token
from sqlmodel import select
from app.core.security import verify_pwd
from app.core.security import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import settings

router = APIRouter(
    tags=['Login']
)

@router.post('/login', response_model=Token)
def login(session: SessionDep , user_credentials : OAuth2PasswordRequestForm = Depends()):

    # {
    #     "username" : email, 
    #     "password" : password
    # }
    # It has now become a form data not a JSON Data.
    # OAuth2PasswordRequestForm converts it into a dictionary like in this format

    statement = select(User).where(User.email == user_credentials.username)
    session_user = session.exec(statement).first()
    if not session_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_pwd(user_credentials.password, session_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(session_user.id, 
                                         expires_delta=access_token_expires)
    )
