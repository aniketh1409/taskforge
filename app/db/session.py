from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)


Base = declarative_base() 
'''
This is the Parent class that the DB models will inherit from
(For sqlalchemy to know which database classes are database tables)
'''


def get_db():
    db = SessionLocal()
    try:
        yield db #provides the db session
    finally:
        db.close()

'''to define how the route functions can safely borrow a session
    creates session - an temp db objec (connection/db session) that is yielded to function/program/route that needs it
'''