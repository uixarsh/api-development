from fastapi import APIRouter, status, HTTPException, Depends
from app.core.db import SessionDep
from app.models import User, Token
from sqlmodel import select
from app.utils import verify_pwd
from app.api.routes import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

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
    
    access_token = oauth2.create_access_token(data={"user_id": session_user.id})
    return {"access_token": access_token, "token_type" : "bearer"}