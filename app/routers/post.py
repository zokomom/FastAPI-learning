from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from typing import Optional
from sqlalchemy import func
# from ..database import cursor

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

router=APIRouter(
    prefix="/posts",
    tags=['post']
)

@router.get("/",response_model=list[schemas.PostOut])
def get_all_posts(db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM POSTS""")
    # return {"data":cursor.fetchall()}
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Post.id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results
    
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post : schemas.PostCreate,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(owner_id=current_user.user_id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post_by_id(id:int,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post=cursor.fetchone()
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    result=db.query(models.Post,func.count(models.Post.id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return result

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(id,))
    # delete_post=cursor.fetchone()
    # conn.commit()
    delete_post=db.query(models.Post).filter(models.Post.id==id).first()

    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists")

    if delete_post.owner_id != current_user.user_id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    db.delete(delete_post)
    db.commit()

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_posts(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exists") 
    post_query.update(post.dict(),synchronize_session=False)
    
    if updated_post.owner_id != current_user.user_id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    db.commit()
    return post_query.first()
