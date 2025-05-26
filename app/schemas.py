from sqlmodel import Field, SQLModel
from datetime import timezone
import datetime

class PostBase(SQLModel):
    title: str = Field(default=None, index=True)
    content: str = Field(default=None)
    published: bool = Field(default=False, nullable=True)
    created_at: datetime.datetime = Field(default_factory = lambda: datetime.datetime.now(timezone.utc))
    
class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class PostPublic(PostBase):
    id: int

class PostCreate(PostBase):
    title: str 
    content: str

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
