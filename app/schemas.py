from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint

class PostsBaseSchema(BaseModel):
    title:str
    content:str
    published : bool=True

class PostCreate(PostsBaseSchema):
    pass

class PostUpdate(PostsBaseSchema):
    pass

class UsersOut(BaseModel):
    user_id:int
    email:EmailStr
    created_at:datetime

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner_id:int
    owner:UsersOut
    model_config={
        "from_attributes":True
    }
class UsersCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)