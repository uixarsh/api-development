from typing import Annotated
from sqlmodel import Session
from sqlmodel import create_engine
from fastapi import Depends
from app.core.config import settings

# DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'
# engine = create_engine(DATABASE_URL)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]