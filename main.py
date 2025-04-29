from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_post = [
    {   
        "id" : 1,
        "title": "something great",
        "content" : "you unlocked a card"
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

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"data not found with id : {id}")

@app.get("/posts")
def get_all_posts():
    return {"data" : my_post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    datas = post.model_dump()
    datas['id'] = randrange(0,10000000)
    my_post.append(datas)
    return {"data" : datas}

@app.delete('/posts/{id}')
def delete_post(id : int):
    post = find_post(id)
    if post:
        my_post.remove(post)
        return {"data" : post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"data not found with id : {id}")

def find_post(id : int) -> dict:
    for post_data in my_post:
        if post_data['id'] == id:
            return post_data