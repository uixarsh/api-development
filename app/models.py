from sqlmodel import Field, SQLModel

class PostBase(SQLModel):
    title: str = Field(default=None, index=True)
    content: str = Field(default=None)
    published: bool = False
    
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
