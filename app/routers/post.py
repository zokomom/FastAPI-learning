from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2

router=APIRouter(
    prefix="/posts",
    tags=['post']
)

@router.get("/",response_model=list[schemas.Post])
def get_all_posts(db:Session=Depends(get_db),get_access_token : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM POSTS""")
    # return {"data":cursor.fetchall()}
    return db.query(models.Post).all() 

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post : schemas.PostCreate,db:Session=Depends(get_db),get_access_token : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post_by_id(id:int,db:Session=Depends(get_db),get_access_token : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),get_access_token : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(id,))
    # delete_post=cursor.fetchone()
    # conn.commit()
    delete_post=db.query(models.Post).filter(models.Post.id==id).first()
    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists")
    db.delete(delete_post)
    db.commit()

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_posts(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db),get_access_token : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists") 
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
