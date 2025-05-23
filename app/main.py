from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful !")
        break
    except Exception as error:
        print("Connecting to database failed.", error)
        time.sleep(5)


class Post(BaseModel):
    id : int = None
    title : str
    content : str
    is_published : bool = False

@app.get("/")
def root():
    return {"message" : "welcome to the api! "}

@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data" : posts}

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found with id : {id}")
    return {"data" : post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.is_published,))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found with id : {id}")

@app.put('/posts/{id}', status_code=status.HTTP_201_CREATED)
def update_post(id : int, post : Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(post.is_published), str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data not found with id : {id}")
    return {'data' : updated_post}