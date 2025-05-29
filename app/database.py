from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings

#SQL_ALCHEMY_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQL_ALCHEMY_URL="postgresql://postgres:eUigYHvanXQjidOYijnXIYPWvMfJEvQN@centerbeam.proxy.rlwy.net:50015/railway"



engine=create_engine(SQL_ALCHEMY_URL) # that is what connect the postgresql with sqlalchemy

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)   # responsible for talking to the database 

Base=declarative_base()                                                    # serve as base class for all the orm models that all the models will inherit from then turned into tables

def get_db():                                                              # a dependency

    db=SessionLocal()
    try:
        yield db                                                          # yield db: Passes the session to path operation functions.
    finally:
        db.close()    


