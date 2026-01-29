from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

# try : 
#     conn = psycopg.connect(host='localhost',dbname='social_media_database',user='postgres',password='root',row_factory=dict_row)
#     cursor = conn.cursor()
#     print("Database Connected Successfully!")
# except Exception as e:
#     print(e)
# source=[{'title':'college','content':'bekar hai bhot','id':1},{'title':'school','content':'acha hai bhot','id':2}]

# def post_by_id(id):
#     for i in source:
#         if i['id']==id:
#             return i
# def index(id):
#     index_count=-1
#     for i in source:
#         index_count+=1
#         if i['id']==id:
#             return index_count

class Post(BaseModel):
    title:str
    content:str
    published : bool=True

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/sqlalchemy")
# def sqlalchemy(db:Session=Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return posts

@app.get("/posts")
def get_all_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS""")
    # return {"data":cursor.fetchall()}
    return db.query(models.Post).all() 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"created post" : new_post}

@app.get("/posts/{id}")
def get_post_by_id(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return {"data": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(id,))
    # delete_post=cursor.fetchone()
    # conn.commit()
    delete_post=db.query(models.Post).filter(models.Post.id==id).first()
    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists")
    db.delete(delete_post)
    db.commit()

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_posts(id:int,post:Post):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists") 
    
    return {"message" : updated_post}
