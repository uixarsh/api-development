from fastapi import Query, HTTPException, status, APIRouter
from sqlmodel import select
from app.models import User, CreateUser, UserPublic
from app.core.db import SessionDep
from typing import Annotated
from app.utils import get_pwd_hash

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Create User
@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, session: SessionDep):
    user.password = get_pwd_hash(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# Read Users
@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found")
    return users

# Read User
@router.get("/{id}", response_model=UserPublic)
def read_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user