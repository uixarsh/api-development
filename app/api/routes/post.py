from fastapi import Query, HTTPException, status, APIRouter, Depends
from sqlmodel import select
from app.models import Post, PostPublic, CreatePost, UpdatePost
from app.api.deps import CurrentUser, SessionDep
from typing import Annotated, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Create Post
@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, 
                session: SessionDep, 
                current_user : CurrentUser):
    new_post = Post.model_validate(post, update={"owner_id": current_user.id})
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

# Read Posts
@router.get("/", response_model=list[PostPublic])
def read_posts(
    session: SessionDep,
    current_user : CurrentUser,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    search : Optional[str] = ""
    ):
    posts = session.exec(select(Post).where((Post.owner_id == current_user.id) & (Post.title.contains(search))).offset(offset).limit(limit)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found")
    return posts

# Read One Post
@router.get("/{id}", response_model=PostPublic)
def read_post(id: int, 
              session: SessionDep, 
              current_user : CurrentUser):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action!")
    
    return post

# Update Post
@router.put("/{id}", response_model=PostPublic, status_code= status.HTTP_201_CREATED)
def update_post(id: int, 
                update_post: UpdatePost, 
                session: SessionDep, 
                current_user : CurrentUser):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action!")
    
    updated_data = update_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(updated_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# Delete Post
@router.delete("/{id}")
def delete_post(id: int, 
                session: SessionDep,  
                current_user : CurrentUser):
    post = session.get(Post, id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data not found with id : {id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action!")
    
    session.delete(post)
    session.commit()