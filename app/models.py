from sqlmodel import Field, SQLModel, Column, DateTime, func
from pydantic import EmailStr
import datetime

'''
POST TABLE
'''
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


'''
USER TABLE
'''
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    
class User(UserBase, table=True):
    id : int = Field(default=None, primary_key=True)
    password : str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    
class CreateUser(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserPublic(UserBase):
    id : int


'''
AUTHENTICATION
'''
class UserLogin(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password : str