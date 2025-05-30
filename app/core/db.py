from typing import Annotated
from sqlmodel import Session
from sqlmodel import create_engine
from fastapi import Depends
from app.core.config import settings

# DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]