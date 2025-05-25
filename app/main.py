from fastapi import FastAPI, Query, HTTPException, status
from sqlmodel import SQLModel, select
from app.models import Post, PostPublic, PostCreate, PostUpdate
from app.database import engine, SessionDep
from typing import Annotated

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Create Post
@app.post("/posts/", response_model=PostPublic)
def create_post(create_post: PostCreate, session: SessionDep):
    post = Post.model_validate(create_post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# Read Posts
@app.get("/posts/", response_model=list[PostPublic])
def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found")
    return posts

# Read One Post
@app.get("/posts/{id}", response_model=PostPublic)
def read_post(id: int, session: SessionDep):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return post

# Update Post
@app.put("/posts/{id}", response_model=PostPublic, status_code= status.HTTP_201_CREATED)
def update_post(id: int, update_post: PostUpdate, session: SessionDep):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    updated_data = update_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(updated_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# Delete Post
@app.delete("/posts/{id}")
def delete_post(id: int, session: SessionDep, status_code=status.HTTP_204_NO_CONTENT):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data not found with id : {id}")
    session.delete(post)
    session.commit()
