from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from .routers import post, user

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(post.router)
app.include_router(user.router)