import sys
sys.dont_write_bytecode = True

from sqlmodel import SQLModel
from fastapi import FastAPI
from app.api.main import api_router
from app.core.db import engine
from app.core.config import settings

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(api_router)