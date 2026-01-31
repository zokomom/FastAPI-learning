from datetime import datetime
from pydantic import BaseModel

class PostsBaseSchema(BaseModel):
    title:str
    content:str
    published : bool=True

class PostCreate(PostsBaseSchema):
    pass

class PostUpdate(PostsBaseSchema):
    pass

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime

    class Config:
        orm_mode=True   