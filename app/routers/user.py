from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,models,utils
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/users"
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UsersOut)
def create_user(user:schemas.UsersCreate,db:Session=Depends(get_db)):
    new_password=utils.hash(user.password)
    user.password=new_password
    new_user=models.Users(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    return new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UsersOut)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} not found")
    return user