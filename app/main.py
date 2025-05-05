from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

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

@app.get("/posts")
def get_all_posts():
    return {"data" : my_post}

@app.get("/posts/{id}")
def get_post(id : int):
    post_idx = find_post(id)
    if post_idx is not None:
        return my_post[post_idx]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"data not found with id : {id}")

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    datas = post.model_dump()
    my_post.append(datas)
    return {"data" : datas}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post_idx = find_post(id)
    if post_idx is not None:
        my_post.pop(post_idx)
        return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"data not found with id : {id}")

@app.put('/posts/{id}', status_code=status.HTTP_201_CREATED)
def update_post(id : int, post : Post):
    post_idx = find_post(id)
    new_content = post.model_dump()
    if post_idx is not None:
        my_post[post_idx]['title'] = new_content['title']
        my_post[post_idx]['content'] = new_content['content']
        return my_post[post_idx]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"data not found with id : {id}")
    
def find_post(id : int) -> int:
    '''
        Find the post via UNIQUE Identifier : id 
        Returns the Index if found.
    '''
    for idx, post_data in enumerate(my_post):
        if post_data['id'] == id:
            return idx
    return None