from fastapi import Query, HTTPException, status, APIRouter
from sqlmodel import select
from app.models import Post, PostPublic, CreatePost, UpdatePost
from app.core.db import SessionDep
from typing import Annotated

router = APIRouter()

# Create Post
@router.post("/posts/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, session: SessionDep):
    new_post = Post.model_validate(post)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

# Read Posts
@router.get("/posts/", response_model=list[PostPublic])
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
@router.get("/posts/{id}", response_model=PostPublic)
def read_post(id: int, session: SessionDep):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Update Post
@router.put("/posts/{id}", response_model=PostPublic, status_code= status.HTTP_201_CREATED)
def update_post(id: int, update_post: UpdatePost, session: SessionDep):
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
@router.delete("/posts/{id}")
def delete_post(id: int, session: SessionDep, status_code=status.HTTP_204_NO_CONTENT):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data not found with id : {id}")
    session.delete(post)
    session.commit()