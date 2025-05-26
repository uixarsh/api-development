from sqlmodel import Field, SQLModel, Column, DateTime, func
from pydantic import EmailStr
import datetime

'''
POST TABLE
-----------

CREATE TABLE post (
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN,
    id SERIAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id)
)
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
-----------

CREATE TABLE "user" (
    email VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    full_name VARCHAR(255),
    id SERIAL NOT NULL,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id)
)
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