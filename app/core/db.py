from typing import Annotated
from sqlmodel import Session
from sqlmodel import create_engine
from fastapi import Depends

DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]