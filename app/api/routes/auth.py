from fastapi import APIRouter, status, HTTPException
from app.core.db import SessionDep
from app.models import UserLogin, User
from sqlmodel import select
from app.utils import verify_pwd

router = APIRouter(
    tags=['Login']
)

@router.post('/login')
def login(user_credentials : UserLogin, session: SessionDep):
    statement = select(User).where(User.email == user_credentials.email)
    session_user = session.exec(statement).first()
    if not session_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not verify_pwd(user_credentials.password, session_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # create a token
    # return token
    return {"token": "example token"}