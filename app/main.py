from fastapi import FastAPI
from .database import engine
from .routers import post,user,auth,vote
from . import models
# import psycopg
# from psycopg.rows import dict_row

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

# try : 
#     conn = psycopg.connect(host='localhost',dbname='social_media_database',user='postgres',password='root',row_factory=dict_row)
#     cursor = conn.cursor()
#     print("Database Connected Successfully!")
# except Exception as e:
#     print(e)
# source=[{'title':'college','content':'random','id':1},{'title':'school','content':'acha hai bhot','id':2}]

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}