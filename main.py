from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_post = [
    {   
        "id" : 1,
        "title": "title of post 1",
        "content" : "content of post 1"
    },
    {
        "id" : 2,
        "title" : "favourite foods",
        "content" : "i like pizza"
    }
]

class Post(BaseModel):
    id : int = None
    title : str
    content : str
    published : bool = False
    rating : Optional[int] = None

@app.get("/")
def root():
    return {"message" : "welcome to my api! "}

@app.get("/posts")
def get_posts():
    return {"data" : my_post}

@app.post('/posts')
def create_post(post : Post):
    datas = post.model_dump()
    datas['id'] = randrange(0,10000000)
    my_post.append(datas)
    return {"data" : datas}