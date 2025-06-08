from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from Inovaparq.API.database.db import Base, engine

def createUserTable():
    User.__table__.create(bind = engine, checkfirst = True) 
    
def createStartupTable():
    Startup.__table__.create(bind = engine, checkfirst = True)   

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), unique = True, index = True, nullable = False)
    password = Column(String(50), nullable = False)
    profile = Column(String(10), nullable = False)
    startup_id = Column(Integer, ForeignKey('startups.id', ondelete = 'CASCADE'), nullable = True)
    
class Startup(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False)
    description = Column(String(200), nullable = False)
    incubator = Column(String(10), nullable = False) 
    stage = Column(String(20), nullable = False)