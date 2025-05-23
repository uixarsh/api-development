from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends, FastAPI


# DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]