from sqlmodel import Field, SQLModel, Column, DateTime, func
from pydantic import EmailStr
import datetime

class PostBase(SQLModel):
    title: str = Field(default=None, index=True)
    content: str = Field(default=None)
    published: bool = Field(default=False, nullable=True)
    
    
class Post(PostBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))

class PostPublic(PostBase):
    id: int

class CreatePost(PostBase):
    title: str 
    content: str

class UpdatePost(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class UserBase(SQLModel):
    email : EmailStr = Field(default=None, unique=True)
    name : str = Field(default=None)
    
class User(UserBase, table=True):
    id : int = Field(default=None, primary_key=True)
    password : str = Field(default=None)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    
class CreateUser(UserBase):
    password : str

class UserPublic(UserBase):
    id : int 