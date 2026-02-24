from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings
# import psycopg
# from psycopg.rows import dict_row

# try : 
#     conn = psycopg.connect(host='localhost',dbname='social_media_database',user='postgres',password='root',row_factory=dict_row)
#     cursor = conn.cursor()
#     print("Database Connected Successfully!")
# except Exception as e:
#     print(e)

# source=[{'title':'college','content':'random','id':1},{'title':'school','content':'random','id':2}]

database_url = settings.database_url

if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )
    
DATABASE_URL = database_url

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        