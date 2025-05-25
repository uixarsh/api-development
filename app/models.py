from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
    
class HeroUpdate(SQLModel):
    name: str = None
    age: int = None
    secret_name: str = None
    