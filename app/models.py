from sqlmodel import Field, SQLModel

class PostBase(SQLModel):
    title: str = Field(default=None, index=True)
    content: str = Field(default=None)
    published: bool
    
class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
class PostPublic(PostBase):
    id: int

class PostCreate(PostBase):
    title: str | None 
    content: str | None
    published : bool = False

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: str | None = None
